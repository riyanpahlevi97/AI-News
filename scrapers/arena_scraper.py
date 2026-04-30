from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def fetch_arena_leaderboard():
    """
    Scrapes the current top models from the LMSYS Chatbot Arena leaderboard using Playwright.
    """
    url = "https://arena.ai/leaderboard/text"
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            # Wait until network is idle to ensure the React app has loaded the table
            await page.goto(url, wait_until='networkidle')
            
            # Wait for the leaderboard table to be visible
            await page.wait_for_selector("table tr", timeout=30000)
            
            # Extract rows from the table
            rows = await page.query_selector_all("table tr")
            
            table_md = "| Rank | Model Name | Elo Rating |\n|---|---|---|\n"
            
            # Skip header row (usually the first one)
            for row in rows[1:11]:  # Get top 10 models
                cols = await row.query_selector_all("td")
                if len(cols) >= 4:
                    rank = await cols[0].inner_text()
                    model_raw = await cols[2].inner_text()
                    score_raw = await cols[3].inner_text()
                    
                    # Clean up text (handle newlines from multi-line cells)
                    model_name = model_raw.split('\n')[0].strip()
                    score = score_raw.split('\n')[0].strip()
                    rank = rank.strip()
                    
                    table_md += f"| #{rank} | **{model_name}** | {score} |\n"
            
            results = [{
                'title': "🏆 LMSYS Chatbot Arena Top 10 Leaderboard",
                'url': url,
                'source': 'LMSYS Arena',
                'raw_summary': table_md
            }]
            
            await browser.close()
            return results
    except Exception as e:
        print(f"Error scraping Arena leaderboard with Playwright: {e}")
        return []

# Removed sync wrapper as main loop is async
