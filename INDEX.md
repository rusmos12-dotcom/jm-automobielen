# JM Automobielen Website - Complete Documentation Index

## Quick Navigation

### Start Here
1. **[QUICKSTART.md](QUICKSTART.md)** - 30-second setup and usage guide
2. **[README.md](README.md)** - Full documentation and setup instructions
3. **Open `index.html` in browser** - View the website immediately

### For Developers
1. **[CONFIG.md](CONFIG.md)** - Detailed configuration reference
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete architecture overview
3. **[VERIFICATION.md](VERIFICATION.md)** - Testing and deployment checklist

### Source Code
- **[index.html](index.html)** - Complete website (30KB, all-in-one)
- **[scraper/scrape.py](scraper/scrape.py)** - Instagram scraper script
- **[.github/workflows/sync.yml](.github/workflows/sync.yml)** - GitHub Actions automation

### Data
- **[data/posts.json](data/posts.json)** - Post data (sample data included)
- **[data/images/](data/images/)** - Downloaded images (auto-populated)

---

## File Purposes Quick Reference

### Documentation Files

| File | Size | Purpose | Read Time |
|------|------|---------|-----------|
| [INDEX.md](INDEX.md) | 3KB | Navigation hub | 2 min |
| [QUICKSTART.md](QUICKSTART.md) | 4KB | Quick reference | 5 min |
| [README.md](README.md) | 5KB | Full guide | 10 min |
| [CONFIG.md](CONFIG.md) | 6KB | Configuration | 15 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 12KB | Complete overview | 20 min |
| [VERIFICATION.md](VERIFICATION.md) | 5KB | Testing checklist | 5 min |

### Code Files

| File | Size | Purpose | Language |
|------|------|---------|----------|
| [index.html](index.html) | 30KB | Website | HTML/CSS/JS |
| [scraper/scrape.py](scraper/scrape.py) | 16KB | Instagram scraper | Python |
| [.github/workflows/sync.yml](.github/workflows/sync.yml) | 2KB | CI/CD automation | YAML |
| [requirements.txt](requirements.txt) | 1KB | Dependencies | Text |
| [run-local.sh](run-local.sh) | 2KB | Setup helper | Bash |

### Data Files

| File | Size | Purpose | Format |
|------|------|---------|--------|
| [data/posts.json](data/posts.json) | 4KB | Post database | JSON |
| [.gitignore](.gitignore) | 1KB | Git configuration | Text |

---

## What to Read When

### "I just want to see it work" (5 minutes)
1. Open `index.html` in your browser
2. Read [QUICKSTART.md](QUICKSTART.md)
3. You're done!

### "I want to set up locally" (15 minutes)
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `./run-local.sh`
3. Run scraper: `python scraper/scrape.py --full`
4. Start server: `python -m http.server 8000`

### "I want to deploy to GitHub Pages" (30 minutes)
1. Read [README.md](README.md) - Deployment section
2. Create GitHub repository
3. Push code to main branch
4. Enable GitHub Pages in settings
5. Done! Auto-syncs every hour

### "I want to understand everything" (1-2 hours)
1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Overview
2. Read [README.md](README.md) - Features & setup
3. Read [CONFIG.md](CONFIG.md) - Configuration details
4. Browse [index.html](index.html) - Website code
5. Browse [scraper/scrape.py](scraper/scrape.py) - Scraper code

### "I want to customize it" (varies)
1. Colors: See [CONFIG.md](CONFIG.md) "Colors & Theme"
2. Content: Edit [data/posts.json](data/posts.json)
3. Sections: Edit [index.html](index.html)
4. Keywords: Edit [scraper/scrape.py](scraper/scrape.py)

### "I need to troubleshoot" (varies)
1. Check [QUICKSTART.md](QUICKSTART.md) "Troubleshooting"
2. Check [README.md](README.md) "Features & Setup"
3. Review [VERIFICATION.md](VERIFICATION.md)

---

## Project Statistics

### Code Metrics
- **Total Files**: 16
- **Total Size**: ~80KB (code + docs)
- **Website**: 30KB (single file)
- **Scraper**: 16KB (single file)
- **Documentation**: 25KB (5 files)
- **Configuration**: 5KB (3 files)

### Language Breakdown
- **HTML/CSS/JavaScript**: 30KB
- **Python**: 16KB
- **YAML**: 2KB
- **Markdown**: 25KB
- **Text**: 5KB

### Lines of Code
- **HTML**: ~650 lines
- **CSS**: ~400 lines
- **JavaScript**: ~250 lines
- **Python**: ~400 lines
- **Total**: ~1700 lines

### Documentation
- **Markdown**: 6 files, 30KB
- **Code comments**: Throughout
- **Examples**: Extensive

---

## Key Features at a Glance

### Website
- Responsive design (mobile/tablet/desktop)
- Dark professional theme
- Dynamic content from JSON
- Auto-categorization
- Price & plate extraction
- 6 main sections
- Smooth navigation
- Zero dependencies

### Scraper
- Instagram profile scraping
- Image downloading
- Auto-categorization (7 categories)
- Car info extraction
- Idempotent (safe to repeat)
- Optional Instagram login
- Comprehensive logging
- Error handling

### GitHub Actions
- Hourly auto-sync
- Manual trigger available
- Auto-deployment
- Change detection
- Auto-commit & push
- No configuration needed

### Data
- Structured JSON
- Profile information
- Post metadata
- Car information
- Image references
- Category tags
- Timestamps

---

## Technology Stack

```
Frontend:
├── HTML5 (semantic markup)
├── CSS3 (grid, flexbox, animations)
└── JavaScript (vanilla, no frameworks)

Backend/Scraping:
├── Python 3.8+
├── Playwright (browser automation)
├── Asyncio (concurrency)
└── JSON (data format)

DevOps/Deployment:
├── GitHub Pages (hosting)
├── GitHub Actions (CI/CD)
├── Git (version control)
└── Bash (automation)
```

---

## Common Tasks & Where to Find Answers

| Task | File | Section |
|------|------|---------|
| View website | [index.html](index.html) | Open in browser |
| Quick setup | [QUICKSTART.md](QUICKSTART.md) | Top |
| Full setup | [README.md](README.md) | Setup section |
| Change colors | [CONFIG.md](CONFIG.md) | Colors & Theme |
| Deploy to GitHub | [README.md](README.md) | GitHub Pages Deployment |
| Run scraper | [QUICKSTART.md](QUICKSTART.md) | Usage Examples |
| Understand scraper | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Component 2 |
| Fix problems | [QUICKSTART.md](QUICKSTART.md) | Troubleshooting |
| See all options | [CONFIG.md](CONFIG.md) | All sections |
| Verify setup | [VERIFICATION.md](VERIFICATION.md) | Checklists |

---

## File Dependencies

```
index.html
  ├── (no external dependencies)
  └── reads: data/posts.json
     
scraper/scrape.py
  ├── requires: playwright
  └── writes: data/posts.json, data/images/*

.github/workflows/sync.yml
  ├── runs: scraper/scrape.py
  ├── updates: data/posts.json
  └── deploys: index.html + data/posts.json

data/posts.json
  ├── read by: index.html
  ├── written by: scraper/scrape.py
  ├── references: data/images/*
  └── format: JSON
```

---

## Getting Help

### Documentation First
1. **[QUICKSTART.md](QUICKSTART.md)** - Fastest answers
2. **[README.md](README.md)** - Comprehensive guide
3. **[CONFIG.md](CONFIG.md)** - Detailed reference
4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Deep dive

### Common Issues
- Check [QUICKSTART.md](QUICKSTART.md) Troubleshooting
- Check [VERIFICATION.md](VERIFICATION.md) Testing section
- Review [CONFIG.md](CONFIG.md) relevant section

### Information You Need
- **Architecture**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Customization**: See [CONFIG.md](CONFIG.md)
- **Setup**: See [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)
- **Deployment**: See [README.md](README.md) GitHub Pages section

---

## About This Project

**Name**: JM Automobielen Website
**Type**: Car Dealer Website with Instagram Sync
**Status**: Complete & Production Ready
**Version**: 1.0
**Created**: March 29, 2026

**For**: JM Automobielen (RDW-recognized car dealer)
**Location**: Hoogkarspel, Netherlands
**Instagram**: @jm.automobielen
**Manager**: Jordy (@jordymortel)

**Features**:
- Modern responsive website
- Automatic Instagram sync
- Professional dark theme
- Smart auto-categorization
- GitHub Pages deployment
- Zero external API calls

---

## Next Steps

1. **Start Now**:
   - Open [index.html](index.html) in your browser
   - Read [QUICKSTART.md](QUICKSTART.md)

2. **Set Up Locally**:
   - Run `./run-local.sh`
   - Run scraper: `python scraper/scrape.py --full`

3. **Deploy Online**:
   - Create GitHub repository
   - Push to main branch
   - Enable GitHub Pages

4. **Customize**:
   - Edit [data/posts.json](data/posts.json)
   - Modify [index.html](index.html) colors
   - Update scraper keywords

5. **Monitor**:
   - Check GitHub Actions logs
   - Verify sync every hour
   - Review image downloads

---

## Document Map

```
INDEX.md (you are here)
├── QUICKSTART.md (quick reference)
├── README.md (full documentation)
├── CONFIG.md (configuration details)
├── PROJECT_SUMMARY.md (architecture overview)
├── VERIFICATION.md (testing checklist)
│
├── index.html (website source)
├── scraper/scrape.py (scraper source)
│
├── data/posts.json (post database)
└── .github/workflows/sync.yml (automation)
```

---

**Ready to get started? Open [QUICKSTART.md](QUICKSTART.md) or just open `index.html` in your browser!**

Created: March 29, 2026
Last Updated: March 29, 2026
Status: Complete ✅
