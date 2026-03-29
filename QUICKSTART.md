# Quick Start Guide - JM Automobielen Website

## 30-Second Setup

1. **View the website** (no dependencies needed!)
   - Open `index.html` directly in your browser
   - Or run: `python -m http.server 8000` and visit http://localhost:8000

2. **Start scrabing Instagram** (first time)
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   python scraper/scrape.py --full
   ```

3. **View results**
   - Check `data/posts.json` to see scraped data
   - Refresh your browser to see updates on the website

## Automated Setup

Use the provided helper script:
```bash
./run-local.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Download Playwright browsers
- Print helpful commands

## Directory Structure

```
jm-automobielen-site/
├── index.html              ← The website (open in browser)
├── data/
│   ├── posts.json         ← Instagram data (auto-generated)
│   └── images/            ← Downloaded images
├── scraper/
│   └── scrape.py          ← Instagram scraper
├── .github/workflows/
│   └── sync.yml           ← Auto-sync on GitHub Actions
├── requirements.txt       ← Python dependencies
├── README.md             ← Full documentation
└── QUICKSTART.md         ← This file
```

## Key Files Explained

### index.html
- **Size**: ~30KB (all-in-one file)
- **Tech**: Vanilla HTML/CSS/JavaScript
- **No build needed**: Just open in browser
- **Responsive**: Works on mobile, tablet, desktop
- **Sections**: Hero, Cars for Sale, Sold Cars, Detailing, Reviews, About, Contact

### data/posts.json
```json
{
  "last_updated": "...",
  "profile": { ... },
  "posts": [
    {
      "id": "instagram_post_id",
      "category": "te_koop|verkocht|detailing|review|...",
      "caption": "Full Instagram caption",
      "images": ["images/...jpg"],
      "car_info": {
        "make": "Volkswagen",
        "model": "Golf",
        "plate": "34-TN-JZ",
        "price": "19500"
      }
    }
  ]
}
```

### scraper/scrape.py
Python script that:
- Logs into Instagram (optional)
- Scrolls through @jm.automobielen profile
- Extracts post data and images
- Auto-categorizes by keywords
- Updates data/posts.json
- Idempotent (safe to run multiple times)

## Usage Examples

### View the website
```bash
# Option 1: Direct file open
open index.html

# Option 2: Local server
python -m http.server 8000
# Visit http://localhost:8000
```

### Scrape Instagram

**New posts only** (recommended for regular use)
```bash
python scraper/scrape.py
```

**All posts** (use for initial setup)
```bash
python scraper/scrape.py --full
```

**With login credentials** (optional, for private profiles)
```bash
INSTAGRAM_USERNAME=your_username INSTAGRAM_PASSWORD=your_password python scraper/scrape.py
```

### Check data
```bash
# Pretty-print posts.json
python -m json.tool data/posts.json

# Count posts by category
python -c "import json; posts = json.load(open('data/posts.json')); categories = {}; [categories.update({p['category']: categories.get(p['category'], 0) + 1}) for p in posts['posts']]; print(categories)"

# List all post IDs
python -c "import json; posts = json.load(open('data/posts.json')); print('\n'.join(p['id'] for p in posts['posts']))"
```

## Customization

### Colors
Edit `index.html` (around line 60):
- `#d4af37` - Gold accent
- `#2d5a2d` - Dark green
- `#0a1628` - Dark background
- `#f0f0f0` - Light text

### Company Info
Edit `data/posts.json` (profile section) or `index.html` contact details

### Sections
Each section is controlled in `index.html`:
- Search for `<section id="...">`
- Hide a section: add `style="display:none"` to the `<section>` tag
- Move sections: reorder the `<section>` tags

## Deployment

### GitHub Pages (Recommended)
1. Push to GitHub
2. Enable GitHub Pages in settings (main branch)
3. Site auto-deploys
4. Auto-sync runs hourly (via workflow)

### Other Hosting
1. Upload files to your host
2. Set up daily cron job: `python scraper/scrape.py`
3. Copy `data/posts.json` and `images/` to host
4. Site works immediately

### Environment Variables (Optional)
For GitHub Actions, add secrets:
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`

## Troubleshooting

### Website shows "No cars available"
- Scraper hasn't run yet
- Run: `python scraper/scrape.py --full`
- Refresh browser

### Images not showing
- Images need to be downloaded first
- Check `data/images/` folder
- Scraper handles this automatically

### Scraper hangs
- Playwright might be blocked by Instagram rate limiting
- Wait a few minutes and try again
- Consider using official Instagram API for production

### JSON syntax error
- Check `data/posts.json` is valid JSON
- Run: `python -m json.tool data/posts.json`

## Advanced

### Running on a schedule (cron)
```bash
# Add to crontab (runs daily at 3 AM)
0 3 * * * cd /path/to/jm-automobielen-site && python scraper/scrape.py
```

### Running in Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt && playwright install chromium
CMD ["python", "scraper/scrape.py"]
```

### API for programmatic access
The website already provides all data via `data/posts.json`. You can:
- Fetch JSON from your website
- Parse and use the data
- No additional API needed

## Performance

- **Website**: ~30KB (HTML + CSS + JS all in one file)
- **Load time**: <1 second on 3G
- **Browser support**: All modern browsers
- **Mobile**: Fully responsive

## Support & Contributions

- **Issues**: Check GitHub Issues
- **Feature requests**: Create an Issue
- **Questions**: Check README.md

---

**Created for JM Automobielen**
RDW erkend autobedrijf in Hoogkarspel, Nederland
