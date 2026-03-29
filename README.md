# JM Automobielen Website

Automated website for JM Automobielen that syncs with their Instagram profile.

## How it works

1. A GitHub Actions workflow runs every hour
2. It scrapes the public Instagram profile `@jm.automobielen` (no login required)
3. Posts are auto-categorized (Te Koop, Verkocht, Detailing, Reviews, etc.)
4. Images are downloaded locally to avoid hotlink blocking
5. The static website reads from `data/posts.json` and displays everything

## Setup

1. Push this repo to GitHub
2. Enable GitHub Pages (Settings → Pages → Source: main branch, root `/`)
3. The GitHub Action will run automatically every hour

## Manual scraper run

```bash
python scraper/scrape.py
```

No external dependencies needed — uses only Python standard library.

## Project structure

```
index.html              → Main website (single-file HTML/CSS/JS)
data/posts.json         → Auto-generated data from Instagram
data/images/            → Downloaded post images
data/logo.png           → Company logo
scraper/scrape.py       → Instagram scraper (lightweight, no browser needed)
.github/workflows/sync.yml → Hourly automation
```
