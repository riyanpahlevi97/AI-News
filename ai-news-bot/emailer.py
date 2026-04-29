import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

BADGE_COLORS = {
    "anthropic": ("background:#EEEDFE;color:#3C3489", "Anthropic"),
    "openai":    ("background:#EAF3DE;color:#27500A", "OpenAI"),
    "deepmind":  ("background:#FAEEDA;color:#633806", "Google DeepMind"),
    "hf":        ("background:#FAECE7;color:#712B13", "Hugging Face"),
    "mit":       ("background:#E6F1FB;color:#0C447C", "MIT Tech Review"),
}


def _badge(badge_key: str) -> str:
    style, label = BADGE_COLORS.get(badge_key, ("background:#F1EFE8;color:#444441", badge_key))
    return (
        f'<span style="display:inline-block;{style};font-size:11px;'
        f'padding:2px 10px;border-radius:20px;font-weight:500;">{label}</span>'
    )


def _new_tag(text: str) -> str:
    return (
        f'<span style="background:#FCEBEB;color:#791F1F;font-size:10px;'
        f'padding:1px 7px;border-radius:3px;margin-left:6px;">{text}</span>'
    )


def _change_html(change: str) -> str:
    if change.startswith("▲") or change == "Baru masuk":
        color = "#3B6D11"
    elif change.startswith("▼"):
        color = "#A32D2D"
    else:
        color = "#888780"
    return f'<span style="color:{color};font-size:11px;">{change}</span>'


def build_html(
    articles: list[dict],
    leaderboard: list[dict],
    highlight: str,
    new_models: list[str],
) -> str:
    today = datetime.now().strftime("%d %B %Y")
    day_name = datetime.now().strftime("%A")
    new_model_count = len(new_models) + sum(1 for a in articles if a.get("is_new_model"))
    claude_articles = [a for a in articles if a.get("is_claude")]
    top1 = leaderboard[0]["model"] if leaderboard else ""

    subject_extra = ""
    if top1 and "claude" in top1.lower():
        subject_extra = f" | {top1} di #1 Arena"
    elif new_model_count:
        subject_extra = f" | {new_model_count} model baru"

    # Build article rows HTML
    article_rows = ""
    for article in articles:
        new_tag = _new_tag("Model baru") if article.get("is_new_model") else ""
        claude_style = "background:#E6F1FB;" if article.get("is_claude") else ""
        article_rows += f"""
        <tr>
          <td style="padding:14px 0;border-bottom:0.5px solid #e8e6e0;{claude_style}">
            <div style="margin-bottom:5px;">
              {_badge(article['badge'])}
              {new_tag}
            </div>
            <div style="font-size:14px;font-weight:500;color:#1a1a1a;margin-bottom:5px;">
              {article['title']}
            </div>
            <div style="font-size:13px;color:#5f5e5a;line-height:1.5;margin-bottom:6px;">
              {article['summary']}
            </div>
            <a href="{article['url']}" style="font-size:12px;color:#185FA5;text-decoration:none;">
              Baca selengkapnya →
            </a>
          </td>
        </tr>"""

    # Build leaderboard rows HTML
    lb_rows = ""
    for entry in leaderboard:
        row_style = "background:#EEF5FC;" if entry.get("is_claude") else ""
        model_style = "color:#0C447C;font-weight:500;" if entry.get("is_claude") else "font-weight:500;"
        new_tag = _new_tag("Baru") if entry.get("is_new") else ""
        lb_rows += f"""
        <tr style="{row_style}">
          <td style="padding:8px;font-size:13px;color:#888780;width:32px;">{entry['rank']}</td>
          <td style="padding:8px;font-size:13px;{model_style}">{entry['model']}{new_tag}</td>
          <td style="padding:8px;font-size:12px;color:#888780;">{entry['score']}</td>
          <td style="padding:8px;">{_change_html(entry['change'])}</td>
        </tr>"""

    # Claude-specific section
    claude_section = ""
    if claude_articles:
        claude_rows = ""
        for a in claude_articles:
            claude_rows += f"""
            <tr>
              <td style="padding:10px 0;border-bottom:0.5px solid #c8d8ec;">
                <div style="font-size:13px;font-weight:500;color:#0C447C;margin-bottom:3px;">{a['title']}</div>
                <div style="font-size:12px;color:#185FA5;line-height:1.4;">{a['summary']}</div>
              </td>
            </tr>"""
        claude_section = f"""
        <tr><td style="padding:20px 0 10px;">
          <div style="background:#E6F1FB;border-left:3px solid #185FA5;padding:14px 16px;">
            <div style="font-size:11px;font-weight:500;color:#0C447C;text-transform:uppercase;
                        letter-spacing:0.05em;margin-bottom:8px;">Berita Claude hari ini</div>
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              {claude_rows}
            </table>
          </div>
        </td></tr>"""

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daily AI News - {today}</title>
</head>
<body style="margin:0;padding:0;background:#f0efe8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f0efe8;padding:20px 0;">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" border="0"
       style="background:#ffffff;border-radius:12px;overflow:hidden;border:0.5px solid #d3d1c7;">

  <!-- HEADER -->
  <tr>
    <td style="background:#0C447C;padding:22px 28px;">
      <div style="font-size:18px;font-weight:500;color:#E6F1FB;margin-bottom:3px;">
        Daily AI News Briefing
      </div>
      <div style="font-size:12px;color:#85B7EB;">
        {day_name}, {today} · Dirangkum otomatis oleh Claude
      </div>
    </td>
  </tr>

  <!-- STATS -->
  <tr><td style="padding:20px 28px 0;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td width="33%" style="text-align:center;background:#f0efe8;border-radius:8px;padding:12px;">
          <div style="font-size:22px;font-weight:500;color:#1a1a1a;">{len(articles)}</div>
          <div style="font-size:11px;color:#888780;margin-top:2px;">Artikel baru</div>
        </td>
        <td width="4%"></td>
        <td width="33%" style="text-align:center;background:#f0efe8;border-radius:8px;padding:12px;">
          <div style="font-size:22px;font-weight:500;color:#1a1a1a;">{new_model_count}</div>
          <div style="font-size:11px;color:#888780;margin-top:2px;">Model baru terdeteksi</div>
        </td>
        <td width="4%"></td>
        <td width="33%" style="text-align:center;background:#f0efe8;border-radius:8px;padding:12px;">
          <div style="font-size:22px;font-weight:500;color:#1a1a1a;">{"#1" if top1 and "claude" in top1.lower() else top1[:6] if top1 else "—"}</div>
          <div style="font-size:11px;color:#888780;margin-top:2px;">{"Claude di Arena" if top1 and "claude" in top1.lower() else "Top Arena"}</div>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- HIGHLIGHT -->
  <tr><td style="padding:16px 28px 0;">
    <div style="background:#E6F1FB;border-left:3px solid #185FA5;padding:12px 16px;">
      <div style="font-size:11px;font-weight:500;color:#0C447C;text-transform:uppercase;
                  letter-spacing:0.05em;margin-bottom:5px;">Highlight hari ini</div>
      <div style="font-size:13px;color:#0C447C;line-height:1.5;">{highlight}</div>
    </div>
  </td></tr>

  <!-- CLAUDE SECTION (conditional) -->
  <tr><td style="padding:0 28px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      {claude_section}
    </table>
  </td></tr>

  <!-- ARTICLES -->
  <tr><td style="padding:20px 28px 0;">
    <div style="font-size:11px;font-weight:500;color:#888780;text-transform:uppercase;
                letter-spacing:0.06em;padding-bottom:10px;border-bottom:0.5px solid #d3d1c7;">
      Berita terbaru
    </div>
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      {article_rows}
    </table>
  </td></tr>

  <!-- LEADERBOARD -->
  <tr><td style="padding:20px 28px 0;">
    <div style="font-size:11px;font-weight:500;color:#888780;text-transform:uppercase;
                letter-spacing:0.06em;padding-bottom:10px;border-bottom:0.5px solid #d3d1c7;
                margin-bottom:4px;">
      Lmarena.ai leaderboard — top {len(leaderboard)} hari ini
    </div>
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <th style="text-align:left;font-size:11px;font-weight:500;color:#888780;padding:6px 8px;
                   border-bottom:0.5px solid #d3d1c7;">#</th>
        <th style="text-align:left;font-size:11px;font-weight:500;color:#888780;padding:6px 8px;
                   border-bottom:0.5px solid #d3d1c7;">Model</th>
        <th style="text-align:left;font-size:11px;font-weight:500;color:#888780;padding:6px 8px;
                   border-bottom:0.5px solid #d3d1c7;">Skor</th>
        <th style="text-align:left;font-size:11px;font-weight:500;color:#888780;padding:6px 8px;
                   border-bottom:0.5px solid #d3d1c7;">Perubahan</th>
      </tr>
      {lb_rows}
    </table>
  </td></tr>

  <!-- FOOTER -->
  <tr><td style="padding:20px 28px;border-top:0.5px solid #d3d1c7;margin-top:20px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td style="font-size:11px;color:#888780;">
          Dikirim otomatis pukul 05:00 WIB setiap hari
        </td>
        <td style="font-size:11px;color:#888780;text-align:right;">
          AI News Bot · Powered by Claude
        </td>
      </tr>
    </table>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""

    return html, f"Daily AI News - {today}{subject_extra}"


def send_email(html: str, subject: str):
    """Send HTML email via Gmail SMTP using App Password."""
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL", gmail_user)

    if not gmail_user or not gmail_password:
        raise ValueError("GMAIL_USER dan GMAIL_APP_PASSWORD harus diset di .env")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"AI News Bot <{gmail_user}>"
    msg["To"] = recipient

    # Plain text fallback
    plain = f"{subject}\n\nBuka email ini dengan HTML viewer untuk tampilan terbaik."
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    logger.info(f"Sending email to {recipient}...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    logger.info("Email sent successfully.")
