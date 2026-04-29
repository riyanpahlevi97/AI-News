import asyncio
from scrapers.rss_scraper import fetch_rss_news
from scrapers.arena_scraper import fetch_arena_leaderboard
from summarizer import summarize_news
from emailer import send_email_newsletter

async def main():
    print("Starting AI News Bot...")
    
    # 1. Scrape news from RSS feeds
    print("Scraping RSS feeds...")
    rss_news = fetch_rss_news()
    
    # 2. Scrape Arena Leaderboard
    print("Scraping Arena leaderboard...")
    arena_news = await fetch_arena_leaderboard()
    
    # Combine all gathered news
    all_news = rss_news + arena_news
    print(f"Gathered {len(all_news)} news items.")
    
    if not all_news:
        print("No news found. Skipping summarization and email.")
        return

    # 3. Summarize news using AI
    print("Summarizing news...")
    summary = summarize_news(all_news)
    
    # 4. Send the summary via email
    print("Sending email...")
    success = send_email_newsletter(summary)
    
    if success:
        print("AI News Bot completed successfully!")
    else:
        print("AI News Bot failed to send email.")

if __name__ == "__main__":
    asyncio.run(main())