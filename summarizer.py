import os
from dotenv import load_dotenv

load_dotenv()

def summarize_news(news_items):
    """
    Formats a list of news items into a simple Markdown summary.
    """
    if not news_items:
        return "No new AI news found for the last 24 hours."

    output = "# 🚀 Daily AI News Summary\n\n"
    
    for item in news_items[:15]:
        output += f"- **{item['title']}** [Link]({item['url']}) - {item.get('source', 'Unknown Source')}\n"
    
    return output
