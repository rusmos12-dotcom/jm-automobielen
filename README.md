# JM Automobielen Website

Automated website for JM Automobielen that syncs with their Instagram profile.

## How it works

1. A GitHub Actions workflow runs every hour
2. It scrapes the public Instagram profile `@jm.automobielen`
3. Posts are auto-categorized (Te Koop, Verkocht, Detailing, Reviews, etc.)
4. The static website reads from `data/posts.json` and displays everything

## Setup

1. Push this repo to GitHub
2. Enable GitHub Pages (Settings → Pages → Source: main branch, root `/`)
3. The GitHub Action will run automatically every hour

## Manual scraper run

```bash
pip install playwright
playwright install chromium
python scraper/scrape.py
```

## Project structure

```
index.html              → Main website (single-file HTML/CSS/JS)
data/posts.json         → Auto-generated data from Instagram
data/logo.png           → Company logo
scraper/scrape.py       → Instagram scraper (Playwright)
.github/workflows/sync.yml → Hourly automation
```
