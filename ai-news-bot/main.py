"""
AI News Bot — Main Orchestrator
================================
Jalankan secara lokal:
    python main.py

Atau otomatis setiap hari via GitHub Actions (lihat .github/workflows/ai_news.yml)
"""

import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ai_news_bot")


def validate_env():
    """Pastikan semua environment variable yang dibutuhkan sudah diset."""
    required = ["ANTHROPIC_API_KEY", "GMAIL_USER", "GMAIL_APP_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        logger.error(f"Environment variable belum diset: {', '.join(missing)}")
        logger.error("Salin .env.example ke .env dan isi nilainya.")
        sys.exit(1)


def run():
    validate_env()

    from scrapers import fetch_articles, scrape_leaderboard, detect_new_models
    from summarizer import summarize_articles, generate_highlight
    from emailer import build_html, send_email

    logger.info("=" * 50)
    logger.info("AI NEWS BOT — mulai proses harian")
    logger.info("=" * 50)

    # 1. Ambil artikel dari RSS
    logger.info("STEP 1: Mengambil artikel dari RSS feeds...")
    articles = fetch_articles(hours_back=24)
    if not articles:
        logger.warning("Tidak ada artikel baru ditemukan dalam 24 jam terakhir.")

    # 2. Scrape leaderboard Arena
    logger.info("STEP 2: Scraping lmarena.ai leaderboard...")
    leaderboard = scrape_leaderboard(top_n=10)
    if not leaderboard:
        logger.warning("Leaderboard tidak berhasil diambil, lanjut tanpa data leaderboard.")

    # 3. Deteksi model baru
    logger.info("STEP 3: Mendeteksi model AI baru...")
    new_models = detect_new_models(articles, leaderboard)
    if new_models:
        logger.info(f"Model baru terdeteksi: {', '.join(new_models)}")

    # 4. Summarize artikel dengan Claude API
    logger.info(f"STEP 4: Merangkum {len(articles)} artikel dengan Claude...")
    articles = summarize_articles(articles)

    # 5. Generate highlight
    logger.info("STEP 5: Membuat highlight harian...")
    highlight = generate_highlight(articles, leaderboard)
    logger.info(f"Highlight: {highlight}")

    # 6. Build dan kirim email
    logger.info("STEP 6: Membangun dan mengirim email...")
    html, subject = build_html(
        articles=articles,
        leaderboard=leaderboard,
        highlight=highlight,
        new_models=new_models,
    )
    send_email(html, subject)

    logger.info("=" * 50)
    logger.info("SELESAI — email berhasil dikirim!")
    logger.info("=" * 50)


if __name__ == "__main__":
    run()
