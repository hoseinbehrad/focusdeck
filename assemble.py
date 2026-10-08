import os
from modules.css import CSS_CONTENT
from modules.js_storage import JS_STORAGE
from modules.js_sync import JS_SYNC
from modules.markup import BODY_MARKUP
from modules.js_state_and_timer import JS_STATE_AND_TIMER
from modules.js_timeblock import JS_TIMEBLOCK
from modules.js_skills import JS_SKILLS
from modules.js_backup import JS_BACKUP
from modules.js_views_and_charts import JS_VIEWS_AND_CHARTS
from modules.js_main import JS_MAIN

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FocusDeck — Offline Focus & 10,000 Hours Mastery Deck</title>
  <meta name="description" content="Offline-first dark dashboard focus timer, Cal Newport daily time-block planner, deliberate practice 10,000 hours tracker, and session analytics.">
  <style>
{CSS_CONTENT}
  </style>
</head>
<body>
{BODY_MARKUP}
  <script>
{JS_STATE_AND_TIMER}
{JS_STORAGE}
{JS_TIMEBLOCK}
{JS_SKILLS}
{JS_BACKUP}
{JS_SYNC}
{JS_VIEWS_AND_CHARTS}
{JS_MAIN}
  </script>
</body>
</html>
"""

# index.html: open locally on this PC. site/index.html: what Cloudflare Pages publishes.
os.makedirs('site', exist_ok=True)
for path in ('index.html', os.path.join('site', 'index.html')):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE)

print(f"Successfully generated index.html. Total size: {len(HTML_TEMPLATE)} bytes.")
