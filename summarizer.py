import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def summarize_news(news_items):
    """
    Summarizes AI news items using OpenAI API into a high-quality Markdown format.
    """
    if not news_items:
        return "No new AI news found for the last 24 hours."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare the news items as a string for the prompt
    news_text = "\n".join([f"- {item['title']} ({item['url']})" for item in news_items[:20]])

    prompt = (
        "You are an expert AI news curator. Please summarize the following AI news items "
        "into a concise, engaging, and professional daily newsletter in Markdown format. "
        "Group similar stories together and provide a brief 1-2 sentence summary for each key highlight. "
        "Ensure you include the original links. Use emojis to make it visually appealing. "
        "Start with a catchy title like '# 🚀 Daily AI News Pulse'.\n\n"
        f"News items:\n{news_text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes AI news."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during OpenAI summarization: {e}")
        output = "# 🚀 Daily AI News Summary\n\n"
        output += "> *Note: This is an automatically generated digest. (OpenAI summarization is currently unavailable)*\n\n"
        for item in news_items[:15]:
            output += f"### [{item['title']}]({item['url']})\n"
            output += f"<span class='source'>**Source:** {item.get('source', 'Unknown')} | **Published:** {item.get('published', '')}</span>\n\n"
            summary = item.get('raw_summary', '').strip()
            if summary:
                # Truncate summary if too long
                if len(summary) > 300:
                    summary = summary[:297] + "..."
                output += f"<div class='summary'>{summary}</div>\n\n"
            output += "---\n\n"
        return output