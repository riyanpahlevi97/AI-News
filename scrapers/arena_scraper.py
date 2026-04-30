from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def fetch_arena_leaderboard():
    """
    Scrapes the current top models from the LMSYS Chatbot Arena leaderboard using Playwright.
    """
    url = "https://lmarena.ai/?leaderboard"
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            
            # Wait for the leaderboard table to be visible (Gradio can be slow)
            await page.wait_for_selector("table", timeout=30000)
            
            # Extract rows from the table
            rows = await page.query_selector_all("table tr")
            
            results = []
            # Skip header row (usually the first one)
            for row in rows[1:11]:  # Get top 10 models
                cols = await row.query_selector_all("td")
                if len(cols) >= 2:
                    model_name = await cols[0].inner_text()
                    score = await cols[1].inner_text()
                    
                    results.append({
                        'title': f"Arena Top Model: {model_name.strip()}",
                        'url': url,
                        'source': 'LMSYS Arena',
                        'score': score.strip()
                    })
            
            await browser.close()
            return results
    except Exception as e:
        print(f"Error scraping Arena leaderboard with Playwright: {e}")
        return []

# Removed sync wrapper as main loop is async
