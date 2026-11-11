#!/usr/bin/env python3
"""
build_week.py - weekly learning digests from a local model.

Reads the two syllabi from ./syllabus, asks a local Ollama model for
structured content, and renders one glanceable HTML page per day into
./current. Last week's pages move to ./archive/<week>/ first, and the
folder is committed and pushed if it is a git repository.

No third-party packages. Python 3.9+.

Usage:
  python3 build_week.py                 # build the coming week
  python3 build_week.py --date 2026-11-16   # build the week containing this date
  python3 build_week.py --mock          # no model; placeholder text, to test layout
  python3 build_week.py --force         # rebuild even if this week already exists
  python3 build_week.py --backfill --date 2026-10-19   # build a past week into archive/
"""

import argparse
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ----------------------------------------------------------------- settings

MODEL = "qwen3:14b"            # check `ollama list`; change the tag here if needed
OLLAMA_URL = "http://localhost:11434"
CONTEXT_TOKENS = 16384
TEMPERATURE = 0.5
GIT_PUSH = True

ROOT = Path(__file__).resolve().parent
SYLLABUS = ROOT / "syllabus"
CURRENT = ROOT / "current"
ARCHIVE = ROOT / "archive"

FINANCE_TRACKER = SYLLABUS / "finance-tracker.md"
FINANCE_SYLLABUS = SYLLABUS / "finance-syllabus.md"     # optional, used if present
VISUAL_SYLLABUS = SYLLABUS / "visual-syllabus.md"

FINANCE_START = dt.date(2026, 10, 19)    # Monday of finance real week 1
VISUAL_START = dt.date(2026, 10, 26)     # Monday of visual week 1
VISUAL_BUFFER = dt.date(2026, 12, 21)    # unnumbered buffer week
VISUAL_WEEKS = 28

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
FINANCE_SHAPE = [
    "concept and reading, 1 hour",
    "concept and reading, 1 hour",
    "concept and reading, 1 hour",
    "concept and reading, 1 hour",
    "build 1, 2 hours, produces a file",
    "build 2, 2-3 hours, produces a file",
    "reconcile the week and look ahead, 45 minutes",
]


def log(msg):
    print(f"[{dt.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


# ------------------------------------------------------------ week location

def target_monday(today):
    """On a Sunday, build for the week starting tomorrow. Otherwise this week."""
    if today.weekday() == 6:
        return today + dt.timedelta(days=1)
    return today - dt.timedelta(days=today.weekday())


def week_id(monday):
    iso = monday.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def finance_context(monday):
    """Return (label, source_text) for the finance track this week."""
    real_week = (monday - FINANCE_START).days // 7 + 1
    tracker = FINANCE_TRACKER.read_text(encoding="utf-8")
    row = None
    for line in tracker.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|([^|]+)\|([^|]+)\|([^|]+)\|", line)
        if m and int(m.group(1)) == real_week:
            row = [g.strip() for g in m.groups()]
            break
    if row is None:
        return None, None
    _, dates, syl_weeks, topic = row
    topic = topic.replace("**", "")
    if "buffer" in topic.lower() or not re.search(r"\d", syl_weeks):
        return f"Buffer week ({dates})", "Buffer week: catch up on unfinished deliverables or rest."

    parts = [f"Real week {real_week} ({dates}). Syllabus weeks {syl_weeks}. Topics: {topic}."]
    nums = [int(n) for n in re.findall(r"\d+", syl_weeks)]

    # statistics add-ons and lab companies from the tracker
    for line in tracker.splitlines():
        if line.startswith("- **S") and any(f"Week {n} " in line or f"Week {n}(" in line for n in nums):
            parts.append("Statistics add-on this week: " + line.lstrip("- "))
    lab = re.search(r"## Lab companies.*?(?=\n## )", tracker, re.S)
    if lab:
        parts.append(lab.group(0).strip())

    # full syllabus sections, if the file has been exported
    if FINANCE_SYLLABUS.exists():
        text = FINANCE_SYLLABUS.read_text(encoding="utf-8")
        for n in nums:
            m = re.search(
                rf"^#+[^\n]*\bWeek\s+{n}\b[^\n]*\n.*?(?=^#+[^\n]*\bWeek\s+\d+\b|^#\s|^##\s|\Z)",
                text, re.S | re.M)
            if m:
                parts.append(m.group(0).strip()[:5000])
    return f"Syllabus weeks {syl_weeks}: {topic}", "\n\n".join(parts)


def visual_context(monday):
    """Return (label, source_text) for the visual track this week."""
    if monday == VISUAL_BUFFER:
        return "Buffer week", "Buffer week: catch up or rest. Keep the daily swipe file going."
    n = (monday - VISUAL_START).days // 7 + 1
    if monday > VISUAL_BUFFER:
        n -= 1
    if n < 1 or n > VISUAL_WEEKS:
        return None, None
    text = VISUAL_SYLLABUS.read_text(encoding="utf-8")
    m = re.search(rf"^### Week {n} — .*?(?=^### |^## |^---|\Z)", text, re.S | re.M)
    if not m:
        return None, None
    section = m.group(0).strip()
    title = section.splitlines()[0].replace("### ", "").replace("**", "")
    spine = re.search(r"### The spine.*?(?=^### )", text, re.S | re.M)
    extra = "\n\n" + spine.group(0).strip() if spine else ""
    return title, section + extra


# ------------------------------------------------------------------- model

def ensure_ollama():
    def up():
        try:
            urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=3)
            return True
        except Exception:
            return False
    if up():
        return
    log("Ollama is not responding; trying to start it")
    subprocess.run(["open", "-a", "Ollama"], check=False)
    for _ in range(30):
        time.sleep(2)
        if up():
            return
    raise SystemExit("Ollama did not start. Open the Ollama app and run this again.")


SYSTEM = (
    "You write short study digests for one adult learner who thinks visually. "
    "Plain, direct British English. No hype, no filler, no rhetorical questions. "
    "Use only facts, names and figures that appear in the source material. "
    "Where you need numbers for a worked example, invent small round ones and "
    "say they are illustrative. Never state real company figures. "
    "Reply with JSON only, matching the schema."
)


def ask(prompt, schema, retries=3):
    body = json.dumps({
        "model": MODEL,
        "stream": False,
        "format": schema,
        "options": {"temperature": TEMPERATURE, "num_ctx": CONTEXT_TOKENS},
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
    }).encode()
    last = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(OLLAMA_URL + "/api/chat", data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=1800) as r:
                content = json.loads(r.read())["message"]["content"]
            data = json.loads(content)
            for key in schema.get("required", []):
                if key not in data:
                    raise ValueError(f"missing field: {key}")
            return data
        except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError) as e:
            last = e
            log(f"  attempt {attempt} failed: {e}")
            time.sleep(3)
    raise SystemExit(f"Model call failed after {retries} attempts: {last}")


def S(**props):
    return {"type": "object", "properties": props, "required": list(props)}


STR = {"type": "string"}
OUTLINE_FIN = S(days={"type": "array", "minItems": 7, "maxItems": 7,
                      "items": S(title=STR, focus=STR)})
OUTLINE_VIS = S(days={"type": "array", "minItems": 7, "maxItems": 7,
                      "items": S(title=STR, prompt=STR, why=STR)})
CARD = S(
    headline=STR, one_thing=STR, narration=STR,
    ideas={"type": "array", "minItems": 3, "maxItems": 3, "items": S(label=STR, text=STR)},
    example=S(title=STR,
              rows={"type": "array", "minItems": 2, "maxItems": 6,
                    "items": S(label=STR, value=STR)},
              takeaway=STR),
    flow={"type": "array", "minItems": 3, "maxItems": 5, "items": S(step=STR, note=STR)},
    do_today=STR, handoff=STR, summary=STR,
)

CARD_RULES = """
Field rules:
- headline: a claim, not a topic. At most 10 words.
- one_thing: the single sentence to remember. At most 22 words.
- narration: 90 to 130 words of connected prose. Open by linking from yesterday
  (or from last week on Monday). No lists.
- ideas: exactly three. label is 1 to 3 words; text is one sentence.
- example: a small worked example. rows are label and value pairs, read top to
  bottom like a short ledger. takeaway is one sentence.
- flow: three to five steps that happen in order. step is 2 to 5 words; note is
  one short sentence.
- do_today: the concrete task for this session and the file it should produce.
- handoff: one sentence that leads into tomorrow's topic.
- summary: one sentence recap, used as context for the next day.
"""


def build_finance(label, source, mock):
    if mock:
        outline = [{"title": f"Finance topic {i + 1}", "focus": "placeholder"} for i in range(7)]
    else:
        log("finance: outline")
        shape = "\n".join(f"- {d}: {s}" for d, s in zip(DAYS, FINANCE_SHAPE))
        outline = ask(
            f"Plan seven daily sessions for this week of a business and finance course.\n\n"
            f"SOURCE MATERIAL\n{source}\n\nWEEK SHAPE\n{shape}\n\n"
            "Spread the week's topics across Monday to Thursday so each day builds on "
            "the one before. Friday and Saturday are builds that apply those concepts "
            "to the lab companies. Sunday reconciles and previews next week. "
            "title is at most 7 words; focus is one sentence on what that day covers.",
            OUTLINE_FIN)["days"]

    cards, prev = [], "This is the first session of the week."
    for i, day in enumerate(outline):
        nxt = outline[i + 1]["title"] if i < 6 else "next week's topics"
        if mock:
            cards.append(mock_card(day["title"]))
            continue
        log(f"finance: {DAYS[i]} - {day['title']}")
        card = ask(
            f"Write the digest for {DAYS[i]}.\n\n"
            f"TODAY: {day['title']} - {day['focus']}\n"
            f"SESSION TYPE: {FINANCE_SHAPE[i]}\n"
            f"YESTERDAY: {prev}\nTOMORROW: {nxt}\n\n"
            f"SOURCE MATERIAL\n{source}\n{CARD_RULES}", CARD)
        prev = card["summary"]
        cards.append(card)
    return outline, cards


def build_visual(label, source, mock):
    if mock:
        outline = [{"title": f"Swipe lens {i + 1}", "prompt": "Save one visual and name the pattern.",
                    "why": "placeholder"} for i in range(7)]
        return outline, mock_card("Visual build session")
    log("visual: outline")
    outline = ask(
        "Plan the week for a visual-creation course. The learner does a 10 minute "
        "swipe-file habit Monday to Friday (save one visual seen that day and write "
        "one line about it), a 15 minute swipe-file review on Saturday, and one "
        "2 to 3 hour build session on Sunday.\n\n"
        f"SOURCE MATERIAL\n{source}\n\n"
        "Return seven entries, Monday to Sunday. For Monday to Friday give each day "
        "a different lens drawn from this week's concepts. title is at most 6 words; "
        "prompt is the instruction for that day in one or two sentences; why is one "
        "sentence on what the lens trains.",
        OUTLINE_VIS)["days"]
    log("visual: Sunday build session")
    sunday = ask(
        "Write the digest for Sunday's 2 to 3 hour build session of a "
        "visual-creation course.\n\n"
        f"SOURCE MATERIAL\n{source}\n\n"
        "The example should be a small before/after or a spec (for instance a type "
        "scale or palette) written as label and value rows. The flow is the order "
        "of work for the session. do_today lists the deliverables from the source "
        "material exactly.\n" + CARD_RULES, CARD)
    return outline, sunday


def mock_card(title):
    return {
        "headline": title,
        "one_thing": "Placeholder sentence standing in for the one idea to remember today.",
        "narration": "Placeholder narration. " * 14,
        "ideas": [{"label": f"Idea {n}", "text": "One sentence explaining it."} for n in (1, 2, 3)],
        "example": {"title": "Worked example (illustrative)",
                    "rows": [{"label": "Revenue", "value": "£100"},
                             {"label": "Costs", "value": "£80"},
                             {"label": "Profit", "value": "£20"}],
                    "takeaway": "One sentence on what the example shows."},
        "flow": [{"step": f"Step {n}", "note": "Short note."} for n in (1, 2, 3, 4)],
        "do_today": "The task for this session and the file it produces.",
        "handoff": "One sentence leading into tomorrow.",
        "summary": "Recap.",
    }


# ------------------------------------------------------------------ render

E = html.escape

CSS = """
:root{color-scheme:light dark;
 --bg:#EEF1F4;--surface:#FFFFFF;--ink:#16202A;--muted:#5B6875;--line:#D5DCE3;
 --fin:#0E6B5C;--vis:#6B3FA0;--mark:#F2C230;--mark-ink:#16202A;
 --display:"Bricolage Grotesque",system-ui,-apple-system,"Segoe UI",sans-serif;
 --text:"Source Serif 4",Georgia,"Times New Roman",serif}
@media (prefers-color-scheme:dark){:root{
 --bg:#10161C;--surface:#18212A;--ink:#E8EDF2;--muted:#93A1AF;--line:#2A3642;
 --fin:#5FC9B5;--vis:#B79AE6}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--text);
 font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
main{max-width:860px;margin:0 auto;padding:24px 18px 64px}
nav{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:28px;
 font-family:var(--display);font-size:14px}
nav a{padding:6px 12px;border-radius:999px;text-decoration:none;color:var(--muted);
 border:1px solid var(--line)}
nav a:hover{color:var(--ink);border-color:var(--muted)}
nav a:focus-visible{outline:2px solid var(--fin);outline-offset:2px}
nav a[aria-current]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
nav .home{margin-right:auto;border:0;padding-left:0;font-weight:600;color:var(--ink)}
.date{font-family:var(--display);color:var(--muted);font-size:15px;margin:0 0 6px}
section{margin-top:40px}
.track{font-family:var(--display);font-size:14px;font-weight:600;margin:0 0 10px}
.fin .track{color:var(--fin)}.vis .track{color:var(--vis)}
h1,h2{font-family:var(--display);font-weight:700;letter-spacing:-.02em;
 line-height:1.08;margin:0 0 18px}
h1{font-size:clamp(34px,7vw,56px)}h2{font-size:clamp(28px,5.5vw,42px)}
.one{font-size:clamp(20px,3.4vw,25px);line-height:1.45;margin:0 0 24px;max-width:30em}
.one span{background:linear-gradient(transparent 12%,var(--mark) 12%,var(--mark) 92%,transparent 92%);
 color:var(--mark-ink);padding:0 .15em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.narr{max-width:38em;margin:0 0 28px}
.ideas{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:0 0 28px;
 border-top:2px solid var(--ink)}
.ideas div{padding:14px 16px 4px 0}
.ideas div+div{padding-left:16px;border-left:1px solid var(--line)}
.ideas b{display:block;font-family:var(--display);font-size:17px;margin-bottom:4px}
.ideas p{margin:0;font-size:15.5px;line-height:1.5;color:var(--muted)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:0 0 24px}
.box{background:var(--surface);border-radius:14px;padding:20px 22px}
.box h3{font-family:var(--display);font-size:16px;margin:0 0 12px}
table{width:100%;border-collapse:collapse;font-family:var(--display);font-size:15.5px}
td{padding:7px 0;border-bottom:1px solid var(--line);vertical-align:top}
td:last-child{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;
 padding-left:12px;white-space:nowrap}
tr:last-child td{border-bottom:0}
.take{font-size:15px;color:var(--muted);margin:12px 0 0}
ol.flow{list-style:none;margin:0;padding:0;counter-reset:s}
ol.flow li{counter-increment:s;position:relative;padding:0 0 14px 38px}
ol.flow li::before{content:counter(s);position:absolute;left:0;top:1px;width:25px;height:25px;
 border-radius:50%;display:grid;place-items:center;font-family:var(--display);
 font-size:13px;font-weight:700;color:var(--surface)}
.fin ol.flow li::before{background:var(--fin)}.vis ol.flow li::before{background:var(--vis)}
ol.flow li:not(:last-child)::after{content:"";position:absolute;left:12px;top:28px;
 bottom:2px;width:1px;background:var(--line)}
ol.flow b{font-family:var(--display);font-size:15.5px;display:block}
ol.flow span{font-size:14.5px;color:var(--muted);line-height:1.45;display:block}
.do{border-left:4px solid;padding:4px 0 4px 16px;margin:0 0 18px;max-width:38em}
.fin .do{border-color:var(--fin)}.vis .do{border-color:var(--vis)}
.do b{font-family:var(--display);font-size:15px;display:block}
.hand{color:var(--muted);font-style:italic;max-width:38em;margin:0}
.mini{background:var(--surface);border-radius:14px;padding:20px 22px}
.mini h2{font-size:24px;margin-bottom:8px}
.mini p{margin:0 0 6px;max-width:36em}.mini .why{color:var(--muted);font-size:15px}
.week{list-style:none;padding:0;margin:24px 0 0;border-top:2px solid var(--ink)}
.week li{border-bottom:1px solid var(--line)}
.week a{display:grid;grid-template-columns:120px 1fr;gap:4px 16px;padding:14px 0;
 text-decoration:none;color:inherit}
.week a:hover .t{text-decoration:underline}
.week .d{font-family:var(--display);color:var(--muted);font-size:15px}
.week .t{font-family:var(--display);font-weight:600;font-size:18px;line-height:1.3}
.week .v{grid-column:2;color:var(--muted);font-size:15px}
@media (max-width:640px){.ideas,.pair{grid-template-columns:1fr}
 .ideas div+div{padding-left:0;border-left:0;border-top:1px solid var(--line)}
 .week a{grid-template-columns:1fr}.week .v{grid-column:1}}
@media print{nav{display:none}body{background:#fff}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;1,8..60,400&display=swap" rel="stylesheet">')


def page(title, nav, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title>{FONTS}<style>{CSS}</style></head>'
            f'<body><main>{nav}{body}</main></body></html>')


def nav_html(active=None, root="../"):
    week_cur = ' aria-current="page"' if active is None else ""
    links = [f'<a class="home" href="{root}index.html">All weeks</a>',
             f'<a href="index.html"{week_cur}>Week</a>']
    for i, d in enumerate(DAYS):
        cur = ' aria-current="page"' if i == active else ""
        links.append(f'<a href="{d.lower()}.html"{cur}>{d}</a>')
    return "<nav>" + "".join(links) + "</nav>"


def full_card(card, cls, track, heading="h2"):
    ideas = "".join(f"<div><b>{E(i['label'])}</b><p>{E(i['text'])}</p></div>" for i in card["ideas"])
    rows = "".join(f"<tr><td>{E(r['label'])}</td><td>{E(r['value'])}</td></tr>"
                   for r in card["example"]["rows"])
    flow = "".join(f"<li><b>{E(s['step'])}</b><span>{E(s['note'])}</span></li>" for s in card["flow"])
    return f"""
<section class="{cls}">
<p class="track">{E(track)}</p>
<{heading}>{E(card['headline'])}</{heading}>
<p class="one"><span>{E(card['one_thing'])}</span></p>
<p class="narr">{E(card['narration'])}</p>
<div class="ideas">{ideas}</div>
<div class="pair">
 <div class="box"><h3>{E(card['example']['title'])}</h3><table>{rows}</table>
  <p class="take">{E(card['example']['takeaway'])}</p></div>
 <div class="box"><h3>How it runs</h3><ol class="flow">{flow}</ol></div>
</div>
<div class="do"><b>Today's session</b>{E(card['do_today'])}</div>
<p class="hand">{E(card['handoff'])}</p>
</section>"""


def mini_card(entry, track):
    return f"""
<section class="vis">
<p class="track">{E(track)}</p>
<div class="mini"><h2>{E(entry['title'])}</h2>
<p>{E(entry['prompt'])}</p><p class="why">{E(entry['why'])}</p></div>
</section>"""


def render(monday, fin, vis, out=CURRENT):
    out.mkdir(parents=True, exist_ok=True)
    root = "../" * len(out.relative_to(ROOT).parts)
    fin_label, fin_outline, fin_cards = fin
    vis_label, vis_outline, vis_sunday = vis
    rows = []
    for i, d in enumerate(DAYS):
        date = monday + dt.timedelta(days=i)
        body = f'<p class="date">{date:%A %-d %B %Y}</p>'
        ftitle = vtitle = ""
        if fin_cards:
            body += full_card(fin_cards[i], "fin", "Business and finance · " + fin_label, "h1")
            ftitle = fin_cards[i]["headline"]
        if vis_outline:
            if i == 6 and vis_sunday:
                body += full_card(vis_sunday, "vis", "Visual creation · " + vis_label)
                vtitle = vis_sunday["headline"]
            else:
                kind = "Swipe file, 15 minute review" if i == 5 else "Swipe file, 10 minutes"
                body += mini_card(vis_outline[i], f"Visual creation · {kind}")
                vtitle = vis_outline[i]["title"]
        (out / f"{d.lower()}.html").write_text(
            page(f"{d} {date:%-d %b} - {ftitle or vtitle}", nav_html(i, root), body), encoding="utf-8")
        rows.append(f'<li><a href="{d.lower()}.html"><span class="d">{date:%a %-d %b}</span>'
                    f'<span class="t">{E(ftitle or vtitle)}</span>'
                    + (f'<span class="v">Visual: {E(vtitle)}</span>' if ftitle and vtitle else "")
                    + "</a></li>")
    end = monday + dt.timedelta(days=6)
    body = (f'<p class="date">Week of {monday:%-d %B} to {end:%-d %B %Y}</p>'
            f'<h1>Seven days, two tracks</h1>'
            + (f'<p class="narr"><b>Finance:</b> {E(fin_label)}</p>' if fin_label else "")
            + (f'<p class="narr"><b>Visual:</b> {E(vis_label)}</p>' if vis_label else "")
            + f'<ul class="week">{"".join(rows)}</ul>')
    (out / "index.html").write_text(page(f"Week of {monday:%-d %b}", nav_html(None, root), body),
                                        encoding="utf-8")
    (out / "week.json").write_text(json.dumps({
        "id": week_id(monday), "monday": monday.isoformat(), "model": MODEL,
        "built": dt.datetime.now().isoformat(timespec="seconds"),
        "finance": {"label": fin_label, "outline": fin_outline, "cards": fin_cards},
        "visual": {"label": vis_label, "outline": vis_outline, "sunday": vis_sunday},
    }, indent=1, ensure_ascii=False), encoding="utf-8")


def write_home():
    """Root index.html listing every built week, newest first."""
    weeks = []
    for meta in [CURRENT / "week.json", *ARCHIVE.glob("*/week.json")]:
        if meta.exists():
            w = json.loads(meta.read_text(encoding="utf-8"))
            weeks.append((w["monday"], meta.parent, w))
    rows = []
    for monday, folder, w in sorted(weeks, key=lambda x: x[0], reverse=True):
        mon = dt.date.fromisoformat(monday)
        end = mon + dt.timedelta(days=6)
        tag = " · this week" if folder == CURRENT else ""
        fin, vis = w["finance"]["label"], w["visual"]["label"]
        rows.append(f'<li><a href="{folder.relative_to(ROOT).as_posix()}/index.html">'
                    f'<span class="d">{mon:%-d %b} to {end:%-d %b}{tag}</span>'
                    f'<span class="t">{E(fin or vis)}</span>'
                    + (f'<span class="v">Visual: {E(vis)}</span>' if fin and vis else "")
                    + "</a></li>")
    body = (f'<p class="date">{len(rows)} weeks</p><h1>Learning digests</h1>'
            f'<ul class="week">{"".join(rows)}</ul>')
    (ROOT / "index.html").write_text(page("Learning digests", "", body), encoding="utf-8")


# ----------------------------------------------------------- archive + git

def archive_previous(new_id, force):
    meta = CURRENT / "week.json"
    if not meta.exists():
        return
    old_id = json.loads(meta.read_text(encoding="utf-8")).get("id", "unknown")
    if old_id == new_id:
        if not force:
            raise SystemExit(f"{new_id} is already built. Use --force to rebuild it.")
        shutil.rmtree(CURRENT)
        return
    dest = ARCHIVE / old_id
    ARCHIVE.mkdir(exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(CURRENT), str(dest))
    log(f"archived {old_id}")


def git_sync(message):
    if not (ROOT / ".git").exists():
        log("not a git repository; skipping push")
        return
    def git(*args):
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        return
    git("commit", "-m", message)
    if GIT_PUSH:
        r = git("push")
        log("pushed to remote" if r.returncode == 0 else f"push failed: {r.stderr.strip()}")


# -------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="any date in the week to build (YYYY-MM-DD)")
    ap.add_argument("--mock", action="store_true", help="skip the model; placeholder text")
    ap.add_argument("--force", action="store_true", help="rebuild an existing week")
    ap.add_argument("--backfill", action="store_true",
                    help="build a past week (needs --date) into archive/, leaving current/ alone")
    args = ap.parse_args()

    if args.date:
        d = dt.date.fromisoformat(args.date)
        monday = d - dt.timedelta(days=d.weekday())
    else:
        monday = target_monday(dt.date.today())
    wid = week_id(monday)
    log(f"building {wid} (Monday {monday})")

    for f in (FINANCE_TRACKER, VISUAL_SYLLABUS):
        if not f.exists():
            raise SystemExit(f"Missing {f}. See README.md.")

    fin_label, fin_src = finance_context(monday)
    vis_label, vis_src = visual_context(monday)
    if not fin_src and not vis_src:
        raise SystemExit("Both tracks have finished. Nothing to build.")

    meta = CURRENT / "week.json"
    current_id = json.loads(meta.read_text(encoding="utf-8")).get("id") if meta.exists() else None
    if args.backfill:
        if not args.date:
            raise SystemExit("--backfill needs --date.")
        if wid == current_id:
            raise SystemExit(f"{wid} is the current week. Build it without --backfill.")
        if (ARCHIVE / wid / "week.json").exists() and not args.force:
            raise SystemExit(f"{wid} is already archived. Use --force to rebuild it.")
    elif current_id == wid and not args.force:
        raise SystemExit(f"{wid} is already built. Use --force to rebuild it.")

    if not args.mock:
        ensure_ollama()
    # generate first, so a failed run leaves last week's pages in place
    fin = (fin_label, *build_finance(fin_label, fin_src, args.mock)) if fin_src else (None, None, None)
    vis = (vis_label, *build_visual(vis_label, vis_src, args.mock)) if vis_src else (None, None, None)

    if args.backfill:
        out = ARCHIVE / wid
        if out.exists():
            shutil.rmtree(out)
    else:
        out = CURRENT
        archive_previous(wid, args.force)
    render(monday, fin, vis, out)
    write_home()
    log(f"wrote {out / 'index.html'}")
    if not args.mock:
        git_sync(f"Week {wid}" + (" (backfill)" if args.backfill else ""))


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (0, None):
            log(f"STOPPED: {e}")
        raise
