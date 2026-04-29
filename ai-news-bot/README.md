# AI News Bot

Sistem otomasi yang mengumpulkan berita AI terbaru setiap pagi dan mengirimkannya ke email Anda.

## Yang dikirim setiap pagi pukul 05:00 WIB

- Artikel terbaru dari Anthropic, OpenAI, Google DeepMind, Hugging Face, MIT Tech Review
- Ringkasan otomatis per artikel (dibuat oleh Claude)
- Highlight Claude Sonnet & Opus dipisah khusus
- Leaderboard top 10 lmarena.ai + perubahan posisi dari hari sebelumnya
- Deteksi model AI baru yang belum pernah muncul sebelumnya

## Setup

### 1. Clone repo dan install dependencies

```bash
git clone https://github.com/username/ai-news-bot.git
cd ai-news-bot
pip install -r requirements.txt
playwright install chromium
```

### 2. Buat file .env

```bash
cp .env.example .env
```

Isi nilai berikut di `.env`:

| Variable | Keterangan |
|---|---|
| `ANTHROPIC_API_KEY` | API key dari console.anthropic.com |
| `GMAIL_USER` | Email Gmail Anda |
| `GMAIL_APP_PASSWORD` | App Password 16 karakter (bukan password Gmail biasa) |
| `RECIPIENT_EMAIL` | Email tujuan (bisa sama dengan GMAIL_USER) |

**Cara membuat Gmail App Password:**
1. Buka https://myaccount.google.com/security
2. Aktifkan 2-Step Verification
3. Buka https://myaccount.google.com/apppasswords
4. Buat app password baru → salin 16 karakter ke `.env`

### 3. Test jalankan lokal

```bash
python main.py
```

### 4. Setup jadwal otomatis via GitHub Actions

1. Push repo ini ke GitHub (pastikan repo **private**)
2. Buka **Settings → Secrets and variables → Actions**
3. Tambahkan 4 secrets berikut:
   - `ANTHROPIC_API_KEY`
   - `GMAIL_USER`
   - `GMAIL_APP_PASSWORD`
   - `RECIPIENT_EMAIL`
4. Selesai — bot akan berjalan otomatis setiap hari pukul 05:00 WIB

Untuk test manual: buka tab **Actions → Daily AI News → Run workflow**

## Struktur project

```
ai-news-bot/
├── main.py                      # Orchestrator utama
├── summarizer.py                # Ringkasan artikel via Claude API
├── emailer.py                   # Generate HTML email + kirim via Gmail SMTP
├── scrapers/
│   ├── rss_scraper.py           # Ambil artikel dari RSS feeds
│   └── arena_scraper.py        # Scrape leaderboard lmarena.ai (Playwright)
├── data/
│   └── previous_leaderboard.json  # Cache untuk tracking perubahan ranking
├── requirements.txt
├── .env.example
└── .github/
    └── workflows/
        └── ai_news.yml          # GitHub Actions scheduler
```

## Menambah sumber berita baru

Edit `scrapers/rss_scraper.py`, tambahkan ke list `RSS_SOURCES`:

```python
{
    "name": "Nama Sumber",
    "url": "https://contoh.com/rss.xml",
    "badge": "custom",
},
```
