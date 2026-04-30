import markdown

content = """# 🚀 Daily AI News Summary

> *Note: This is an automatically generated digest.*

### [OpenAI announces GPT-5.5 High Architecture](https://openai.com)
<span class='source'>**Source:** OpenAI | **Published:** 30 Apr 2026</span>

<div class='summary'>
We are sharing an overview of the architecture behind our newest models, showcasing significant improvements in multimodal reasoning and efficiency.
</div>

---

### [Hugging Face launches new open evaluation standard](https://huggingface.co)
<span class='source'>**Source:** Hugging Face | **Published:** 29 Apr 2026</span>

<div class='summary'>
AI evals are becoming the new compute bottleneck. Here is our proposed solution to streamline community evaluation pipelines.
</div>

---

### [Google DeepMind introduces new autonomous agent framework](https://deepmind.google)
<span class='source'>**Source:** DeepMind | **Published:** 28 Apr 2026</span>

<div class='summary'>
Our new framework allows agents to learn and adapt to new environments autonomously, without human intervention.
</div>

---

### [Microsoft integrates AI into Windows Kernel](https://blogs.windows.com)
<span class='source'>**Source:** Microsoft | **Published:** 28 Apr 2026</span>

<div class='summary'>
Windows will now feature an AI-driven kernel scheduler that optimizes background processes for seamless battery life.
</div>

---

### [Meta open-sources Muse-Spark multimodal model](https://ai.meta.com)
<span class='source'>**Source:** Meta AI | **Published:** 27 Apr 2026</span>

<div class='summary'>
Muse-Spark is our latest model that rivals proprietary systems in text, image, and audio understanding tasks.
</div>

---

### [🏆 LMSYS Chatbot Arena Top 10 Leaderboard](https://arena.ai/leaderboard/text)
<span class='source'>**Source:** LMSYS Arena | **Published:** Just now</span>

<div class='summary'>

| Rank | Model Name | Elo Rating |
|---|---|---|
| #1 | **claude-opus-4-7-thinking** | 1503 |
| #2 | **claude-opus-4-6-thinking** | 1502 |
| #3 | **claude-opus-4-6** | 1497 |
| #4 | **claude-opus-4-7** | 1495 |
| #5 | **gemini-3.1-pro-preview** | 1493 |
| #6 | **muse-spark** | 1489 |
| #7 | **gpt-5.5-high** | 1488 |
| #8 | **gemini-3-pro** | 1486 |
| #9 | **grok-4.20-beta1** | 1479 |
| #10 | **gpt-5.4-high** | 1478 |

</div>

---
"""

html_content = markdown.markdown(content, extensions=['tables'])

html_template = """<html>
  <head>
    <style>
      body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #e2e8f0; background-color: #0f172a; margin: 0; padding: 40px 20px; }
      .container { max-width: 650px; margin: 0 auto; background-color: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
      h1 { color: #f8fafc; text-align: center; border-bottom: 2px solid #334155; padding-bottom: 20px; margin-bottom: 30px; font-size: 28px; }
      h2, h3 { color: #f1f5f9; margin-top: 30px; }
      a { color: #38bdf8; text-decoration: none; font-weight: 500; }
      a:hover { text-decoration: underline; color: #7dd3fc; }
      .source { color: #94a3b8; font-size: 0.85em; display: block; margin-bottom: 10px; }
      .summary { margin-bottom: 25px; color: #cbd5e1; background-color: #334155; padding: 15px; border-left: 4px solid #38bdf8; border-radius: 0 4px 4px 0; overflow-x: auto; }
      hr { border: 0; height: 1px; background: #334155; margin: 30px 0; }
      .footer { text-align: center; margin-top: 40px; font-size: 0.85em; color: #64748b; }
      table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95em; color: #e2e8f0; }
      table th, table td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #475569; }
      table th { background-color: #0f172a; color: #38bdf8; font-weight: 600; }
      table tr:hover { background-color: rgba(255, 255, 255, 0.05); }
    </style>
  </head>
  <body>
    <div class="container">
      {{html_content}}
      <div class="footer">
        <p>Sent by Daily AI News Bot 🤖</p>
      </div>
    </div>
  </body>
</html>""".replace('{{html_content}}', html_content)

with open('sample_email.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
