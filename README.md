# Learning digests

A local model writes one glanceable page per day for the week ahead, covering
both tracks. Runs every Sunday at 18:00 on your Mac. Nothing leaves the machine
except the `git push` of the finished pages.

## Set up (about 15 minutes, mostly the model download)

1. Move this folder to where it will live, for example `~/learning-digests`.
2. Install Ollama from ollama.com, then pull the model:

       ollama pull qwen3:14b

3. Check the layout without the model:

       python3 build_week.py --mock
       open current/index.html

4. Build a real week (expect 10 to 30 minutes):

       python3 build_week.py --force

5. Schedule it:

       bash install.sh

6. Optional, for the GitHub archive. Create an empty repo on github.com, then:

       git init && git add -A && git commit -m "Start"
       git branch -M main
       git remote add origin git@github.com:YOUR-USER/learning-digests.git
       git push -u origin main

   After that every Sunday run commits and pushes on its own.

## What is where

    syllabus/     the source files the model reads (edit these, not the script)
    current/      this week: index.html plus mon.html to sun.html
    archive/      earlier weeks, one folder each (2026-W47, ...)
    logs/         build.log from scheduled runs

`syllabus/finance-tracker.md` and `syllabus/visual-syllabus.md` are already in
place. For richer finance pages, export the Google Doc as Markdown and save it
as `syllabus/finance-syllabus.md`. The script picks it up if it is there.

## Things to know

- **Model choice.** `qwen3:14b` (about 9 GB) fits on a 24 GB Mac with other
  apps open. `qwen3.6:27b` writes better prose but needs about 18 GB of GPU
  memory, more than a 24 GB Mac allows by default, and loading it with the cap
  raised ran the system out of memory. To change it, edit `MODEL` at the top
  of `build_week.py`. If Activity Monitor shows memory pressure going red
  during a run, pick a smaller model.
- **Sleep.** If the Mac is asleep at 18:00 the job runs when it wakes. If it is
  switched off, the run is skipped; start it by hand with step 4.
- **Failed runs are safe.** The script generates everything before it touches
  `current/`, so a failure leaves last week's pages in place. Check the log.
- **Accuracy.** The model is told to use only what is in the syllabus files and
  to mark worked-example numbers as illustrative. It can still be wrong. Treat
  the pages as a primer for the session, and the book and the accounts as the
  source of truth.
- **Stop the schedule:**
  `launchctl bootout gui/$(id -u)/com.learning-digests.weekly`
