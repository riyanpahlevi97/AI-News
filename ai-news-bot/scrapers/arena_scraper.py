import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

ARENA_URL = "https://lmarena.ai/?leaderboard"
PREVIOUS_DATA_FILE = Path("data/previous_leaderboard.json")


def _load_previous() -> dict:
    """Load previous leaderboard data for change comparison."""
    if PREVIOUS_DATA_FILE.exists():
        try:
            with open(PREVIOUS_DATA_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_current(data: list[dict]):
    """Save current leaderboard for next run comparison."""
    PREVIOUS_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    rank_map = {row["model"]: row["rank"] for row in data}
    with open(PREVIOUS_DATA_FILE, "w") as f:
        json.dump(rank_map, f, indent=2)


def _compute_change(model: str, current_rank: int, previous: dict) -> str:
    """Return change string: ▲ +N, ▼ -N, — sama, or Baru masuk."""
    if model not in previous:
        return "Baru masuk"
    prev_rank = previous[model]
    diff = prev_rank - current_rank  # positive = moved up
    if diff > 0:
        return f"▲ +{diff}"
    elif diff < 0:
        return f"▼ {diff}"
    return "— sama"


def scrape_leaderboard(top_n: int = 10) -> list[dict]:
    """
    Scrape lmarena.ai leaderboard using Playwright.
    Returns list of dicts with rank, model, score, change, is_claude.
    Falls back to empty list on failure.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("Playwright not installed. Run: pip install playwright && playwright install chromium")
        return []

    previous = _load_previous()
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        try:
            logger.info(f"Opening {ARENA_URL}")
            page.goto(ARENA_URL, timeout=60_000, wait_until="domcontentloaded")

            # Wait for leaderboard table — Gradio renders a dataframe
            # Try multiple possible selectors
            table_selector = None
            for selector in [
                "table",
                ".svelte-table table",
                "[data-testid='dataframe'] table",
                ".tabular-data table",
            ]:
                try:
                    page.wait_for_selector(selector, timeout=20_000)
                    table_selector = selector
                    logger.info(f"Found table with selector: {selector}")
                    break
                except PWTimeout:
                    continue

            if not table_selector:
                logger.warning("Table not found, trying to wait longer...")
                page.wait_for_timeout(8_000)
                table_selector = "table"

            # Extract table rows
            rows = page.query_selector_all(f"{table_selector} tbody tr")
            logger.info(f"Found {len(rows)} rows in leaderboard")

            for i, row in enumerate(rows[:top_n], start=1):
                cells = row.query_selector_all("td")
                if len(cells) < 2:
                    continue

                # Column structure varies — extract text from all cells
                cell_texts = [c.inner_text().strip() for c in cells]

                # Try to find model name (usually longest text or specific column)
                # lmarena typically: rank | model | score | ...
                model_name = ""
                score = ""

                if len(cell_texts) >= 3:
                    # Check if first cell is a number (rank)
                    if cell_texts[0].replace(".", "").isdigit():
                        model_name = cell_texts[1]
                        score = cell_texts[2]
                    else:
                        model_name = cell_texts[0]
                        score = cell_texts[1] if len(cell_texts) > 1 else ""
                elif len(cell_texts) == 2:
                    model_name = cell_texts[0]
                    score = cell_texts[1]

                if not model_name:
                    continue

                # Clean score — keep only numeric part
                score_clean = "".join(c for c in score if c.isdigit() or c == ".")
                score_clean = score_clean[:6] if score_clean else "—"

                results.append({
                    "rank": i,
                    "model": model_name,
                    "score": score_clean,
                    "change": _compute_change(model_name, i, previous),
                    "is_claude": "claude" in model_name.lower(),
                    "is_new": model_name not in previous,
                })

        except PWTimeout:
            logger.error("Timeout waiting for leaderboard to load")
        except Exception as e:
            logger.error(f"Error scraping leaderboard: {e}")
        finally:
            browser.close()

    if results:
        _save_current(results)
        logger.info(f"Leaderboard scraped: {len(results)} models")

    return results


def detect_new_models(articles: list[dict], leaderboard: list[dict]) -> list[str]:
    """
    Detect newly mentioned AI models by comparing leaderboard new entries
    and article titles against known models.
    """
    new_models = []

    # New models in leaderboard
    for entry in leaderboard:
        if entry.get("is_new") and not entry["is_claude"]:
            new_models.append(entry["model"])

    # New model mentions in article titles
    model_keywords = ["gpt", "claude", "gemini", "mistral", "llama", "grok",
                      "falcon", "phi", "qwen", "yi-", "deepseek", "cohere"]
    for article in articles:
        title_lower = article["title"].lower()
        if any(kw in title_lower for kw in model_keywords):
            article["is_new_model"] = True

    return list(set(new_models))
