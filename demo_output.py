import asyncio
import sys
import os

# Add the directory containing the script to the python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from scrapers.rss_scraper import fetch_rss_news
from scrapers.arena_scraper import fetch_arena_leaderboard
from summarizer import summarize_news

async def main():
    print("--- DEMO: AI News Bot Output ---")
    
    try:
        print("Scraping RSS feeds...")
        rss_news = fetch_rss_news()
        
        print("Scraping Arena leaderboard...")
        arena_news = await fetch_arena_leaderboard()
        
        all_news = rss_news + arena_news
        print(f"Gathered {len(all_news)} news items.")
        
        if not all_news:
            print("No news found. Demo cannot proceed.")
            return

        print("Summarizing news...")
        summary = summarize_news(all_news)
        
        print("\n" + "="*50)
        print("SIMULATED EMAIL CONTENT:")
        print("="*50)
        print(f"Here is your daily AI news summary:\n\n{summary}")
        print("="*50)
        
    except Exception as e:
        print(f"Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())