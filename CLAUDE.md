# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What it does

`build_week.py` is a single-file Python 3.9+ script that uses only the standard library. Every Sunday it asks a local Ollama model (`MODEL`, default `qwen3:14b` at `localhost:11434`) to write study digests for the week ahead on two parallel learning tracks. It renders them as static HTML in `current/`: `index.html`, `mon.html` to `sun.html`, and `week.json`. The previous week's `current/` moves to `archive/<ISO week id>/`. If the folder is a git repo, the script then commits and pushes. `install.sh` installs a launchd agent (`com.learning-digests.weekly`, Sunday 18:00, `/usr/bin/caffeinate -is /usr/bin/python3` so neither idle sleep nor the end of a background dark wake can stall the model calls, log at `logs/build.log`).

## Commands

Run these from this directory. `ROOT` is the script's own directory, so `syllabus/`, `current/` and `archive/` resolve relative to it, not to the cwd:

```sh
python3 build_week.py --mock                    # no model, no git; placeholder text to check layout
python3 build_week.py --mock --date 2026-11-16  # mock any week (any date in that week)
python3 build_week.py --force                   # real build, overwriting the current week
python3 build_week.py --backfill --date 2026-10-19  # build a past week into archive/<id>/; current/ untouched
open current/index.html
bash install.sh                                 # (re)install the launchd schedule
launchctl kickstart gui/$(id -u)/com.learning-digests.weekly   # trigger the scheduled job now
```

There are no tests, linter or dependencies. `--mock` is the way to check rendering or date logic. A mock run still archives the previous `current/` and writes `week.json` with the real week id. After a mock run, a real build of the same week needs `--force`.

## How it works

**Week selection.** `target_monday`: on a Sunday the script builds the coming week; on any other day it builds the current week. `--date` overrides this. Hard-coded constants map dates to course weeks:
- `FINANCE_START` is real week 1 of finance. Each real week covers two syllabus weeks.
- `VISUAL_START` is visual week 1. Visual week numbers skip the `VISUAL_BUFFER` Monday. There are `VISUAL_WEEKS = 28` weeks in total.

If neither track has content for a week, the script exits.

**Syllabus parsing is regex-based.** Editing the markdown can silently break it. Keep these exact formats:
- `syllabus/finance-tracker.md`:
  - Schedule rows have the form `| <real wk> | <dates> | <syllabus wks> | <topic> |`.
  - A row is treated as a buffer week when its topic contains "buffer" or its syllabus-weeks cell has no digit.
  - Stats add-on lines start with `- **S` and contain `Week N ` or `Week N(`.
  - The `## Lab companies` section runs until the next `## ` heading.
- `syllabus/visual-syllabus.md`:
  - Each week is a `### Week N — ...` heading, with an em dash. Its section ends at the next `### `, `## ` or `---`.
  - The `### The spine` section is appended to every week's context.
- `syllabus/finance-syllabus.md` is optional (a Google Doc export). For each syllabus week, the script takes the first 5000 characters of the section under any heading containing `Week N`.

**Generation pipeline.** The script generates everything first. Archiving and rendering happen only after all model calls succeed, so a failed run leaves last week's pages untouched.
- `ask()` posts to Ollama `/api/chat` with a JSON-schema `format`. It checks only the schema's top-level `required` keys and makes 3 attempts in total.
- `S(**props)` builds an object schema in which every property is required.
- **Finance:** one outline call (`OUTLINE_FIN`, 7 days following `FINANCE_SHAPE`), then 7 sequential `CARD` calls. Each day's `summary` is passed to the next day's call as "YESTERDAY", which links the narration from day to day.
- **Visual:** one outline call (`OUTLINE_VIS`). Mon–Sat render as small "swipe file" cards. Sunday gets one full `CARD` for the build session.
- The `SYSTEM` prompt and `CARD_RULES` set the content style: British English, facts only from the source, worked-example numbers marked as illustrative. Change those strings to change tone or field rules. If you add or rename a `CARD` field, also update `mock_card`, `full_card` and `render`.

**Rendering.** Hand-built HTML strings with inline `CSS`, using Google Fonts. Light and dark mode come from CSS variables, with `--fin` and `--vis` as the track colours. All model text passes through `html.escape` (`E`). Dates use the `%-d` strftime flag, which works on macOS and glibc but not on Windows. `render(..., out)` writes one week's folder, with nav links relative to it ("All weeks" points to the root). After every build, `write_home()` regenerates the root `index.html` from each `week.json` in `current/` and `archive/*/`. To re-render a week after changing the templates, without calling the model, load its `week.json` and call `render` and `write_home` directly.

**Git.** `git_sync` runs `add -A`, commits as `Week <id>` if anything changed, and pushes if `GIT_PUSH` is set. It runs only on non-mock builds. The remote is the public repo `srigoutam-jagannathan/learning-digests` over HTTPS, using `gh` as the credential helper because this Mac has no SSH key for GitHub. GitHub Pages serves the `main` branch root at https://srigoutam-jagannathan.github.io/learning-digests/. The root `index.html` redirects to `current/index.html`, and `.nojekyll` turns off Jekyll processing.
