import logging
import os
import anthropic

logger = logging.getLogger(__name__)

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = """Kamu adalah asisten yang merangkum artikel teknologi AI ke dalam 2-3 kalimat 
dalam Bahasa Indonesia. Ringkasan harus padat, informatif, dan mudah dipahami. 
Jangan gunakan bullet points. Langsung tulis ringkasannya tanpa kalimat pembuka seperti 
'Artikel ini membahas' atau 'Ringkasan:'."""


def summarize_articles(articles: list[dict]) -> list[dict]:
    """
    Summarize each article using Claude API.
    Adds 'summary' field to each article dict.
    Returns articles with summaries filled in.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    for i, article in enumerate(articles):
        title = article["title"]
        raw = article.get("raw_summary", "")

        if not raw and not title:
            article["summary"] = "Ringkasan tidak tersedia."
            continue

        prompt = f"Judul: {title}\n\nKonten: {raw[:800]}"

        try:
            logger.info(f"Summarizing [{i+1}/{len(articles)}]: {title[:60]}...")
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=200,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            article["summary"] = response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Failed to summarize '{title}': {e}")
            # Fallback: use raw summary truncated
            article["summary"] = raw[:200].strip() + "..." if raw else "Ringkasan tidak tersedia."

    return articles


def generate_highlight(articles: list[dict], leaderboard: list[dict]) -> str:
    """
    Ask Claude to write a 1-2 sentence highlight of the most important news today.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    top_titles = "\n".join(f"- {a['title']} ({a['source']})" for a in articles[:5])
    top_models = ", ".join(f"#{e['rank']} {e['model']}" for e in leaderboard[:3]) if leaderboard else "tidak tersedia"

    prompt = f"""Berdasarkan berita AI hari ini dan leaderboard terbaru, tulis 1-2 kalimat highlight 
paling penting dalam Bahasa Indonesia untuk email briefing pagi hari.

Berita utama:
{top_titles}

Top 3 leaderboard: {top_models}

Tulis hanya highlight-nya, tanpa kalimat pembuka."""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        logger.error(f"Failed to generate highlight: {e}")
        return "Berita AI terbaru telah dikumpulkan. Cek ringkasan di bawah."
