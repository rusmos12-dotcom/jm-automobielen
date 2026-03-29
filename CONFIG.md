# Configuration Reference

## Website Customization (index.html)

### Colors & Theme
Modify the CSS variables section (around line 10-380):

```css
/* Primary Colors */
#d4af37   /* Gold/Accent color for headings and highlights */
#2d5a2d   /* Dark green for borders and secondary elements */
#0a1628   /* Very dark blue/black background */

/* Text Colors */
#f0f0f0   /* Light gray for main text */
#b0b0b0   /* Medium gray for secondary text */
#707070   /* Dark gray for muted text */
#a0a0a0   /* Medium-dark gray for subtle text */
```

### Modify Colors
1. Open `index.html`
2. Find the CSS section (line 8-360)
3. Replace color codes:
   - Headings: Change `#d4af37`
   - Borders: Change `#2d5a2d`
   - Background: Change `#0a1628`

### Fonts
Current: System fonts (Apple System, Segoe UI, Roboto, Helvetica)

To change:
```css
font-family: 'Your Font Name', fallback, sans-serif;
```

### Section Visibility
To hide/show sections, find in `index.html`:

```html
<!-- Hide section by adding style -->
<section id="detailing" style="display: none;">
```

## Profile Configuration (data/posts.json)

### Update Profile Info
```json
{
  "profile": {
    "name": "JM Automobielen",
    "bio": "RDW erkend autobedrijf...",
    "followers": 235,
    "posts_count": 75
  }
}
```

Fields:
- `name` - Company name (shown in header and hero)
- `bio` - Company description
- `followers` - Instagram follower count
- `posts_count` - Total Instagram posts

### Post Structure
```json
{
  "id": "unique_post_id",
  "type": "post",
  "category": "te_koop",
  "caption": "Full post caption",
  "date": "2026-03-29",
  "images": ["images/file1.jpg", "images/file2.jpg"],
  "car_info": {
    "make": "Brand",
    "model": "Model",
    "plate": "AA-11-BB",
    "price": "19500"
  }
}
```

Fields:
- `id` - Unique identifier (Instagram post ID)
- `type` - Always "post"
- `category` - Post category (see Categories below)
- `caption` - Full text from Instagram
- `date` - YYYY-MM-DD format
- `images` - Array of local image paths
- `car_info` - Optional car details (only for cars)

### Categories
- `te_koop` - Cars for sale
- `verkocht` - Sold cars
- `detailing` - Detailing/service work
- `reparatie` - Repairs
- `review` - Customer reviews
- `bedrijf` - Company/RDW info
- `overig` - Other/uncategorized

## Scraper Configuration (scraper/scrape.py)

### Settings
```python
INSTAGRAM_PROFILE = "jm.automobielen"  # Profile to scrape
HEADLESS = True                        # Run browser headless
```

### Instagram Authentication (Optional)
Set environment variables:
```bash
export INSTAGRAM_USERNAME="your_username"
export INSTAGRAM_PASSWORD="your_password"
```

Or pass via command:
```bash
INSTAGRAM_USERNAME=user INSTAGRAM_PASSWORD=pass python scraper/scrape.py
```

### Scraper Behavior
- **Incremental**: Only scrapes new posts since last run
- **Full scrape**: Scrapes all available posts
- **Idempotent**: Safe to run multiple times
- **Auto-categorization**: Uses keyword matching

### Keyword Matching

#### Te Koop (For Sale)
```
Keywords: "te koop", "vraagprijs", "voor meer info", "€"
```

#### Verkocht (Sold)
```
Keywords: "verkocht", "blij gemaakt", "nieuwe eigenaar", "opgehaald"
```

#### Detailing
```
Keywords: "polijst", "detailing", "coating", "interieur", "wax",
          "sealing", "swirl", "polish", "menzerna", "gyeon",
          "extractie", "ozon"
```

#### Reparatie (Repairs)
```
Keywords: "storing", "reparatie", "fout", "diagnose", "coding"
```

#### Review
```
Keywords: "review", "beoordeling", "sterren", "⭐"
```

#### Bedrijf (Company)
```
Keywords: "rdw", "erkend", "stap"
```

### Car Information Extraction

The scraper automatically extracts:

#### License Plate
Regex: `[A-Z]{2,3}[-\s]\d{1,3}[-\s][A-Z]{2}`
Example: `34-TN-JZ` or `34 TN JZ`

#### Price
Regex: `€\s*([0-9.]+)`
Example: `€19.500` → `19500`

#### Make & Model
Looks for 60+ car brands (Volkswagen, BMW, Audi, etc.)
Extracts first word after brand as model

### Advanced: Custom Keyword Lists

To add keywords, edit `scrape.py`:

```python
@staticmethod
def _categorize_post(caption: str) -> str:
    caption_lower = caption.lower()

    if any(word in caption_lower for word in ['your_keyword', 'another_keyword']):
        return 'your_category'
```

## GitHub Actions Configuration (.github/workflows/sync.yml)

### Schedule
```yaml
schedule:
  - cron: '0 * * * *'  # Every hour at minute 0
```

Cron format: `minute hour day month weekday`

Examples:
```
'0 * * * *'        # Every hour
'0 9 * * *'        # Daily at 9 AM UTC
'0 9 * * 1-5'      # Weekdays at 9 AM UTC
'0 0 1 * *'        # Monthly on the 1st
```

### GitHub Secrets (Optional)
For authenticated Instagram access:

1. Go to repo Settings → Secrets
2. Add:
   - `INSTAGRAM_USERNAME`
   - `INSTAGRAM_PASSWORD`

Workflow will use these if available.

### Workflow Triggers
- **Schedule**: Every hour (automatic)
- **Manual**: workflow_dispatch (run manually from Actions tab)
- **Push**: On code push to main branch

## Python Dependencies (requirements.txt)

```
playwright==1.40.0
```

That's it! Only one dependency.

To add more:
```
package-name==version
```

Then run:
```bash
pip install -r requirements.txt
```

## Directory Structure Reference

```
jm-automobielen-site/
├── index.html                 # Main website (30KB)
├── data/
│   ├── posts.json            # Post data (auto-generated)
│   └── images/               # Downloaded images
├── scraper/
│   └── scrape.py             # Instagram scraper
├── .github/
│   └── workflows/
│       └── sync.yml          # GitHub Actions automation
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
├── QUICKSTART.md            # Quick start guide
├── CONFIG.md                # This file
└── run-local.sh             # Helper script
```

## Performance Tuning

### Website
- Single HTML file: fast load
- Inline CSS: no additional requests
- Vanilla JS: no framework overhead
- Images: lazy-load ready (add loading="lazy" to img tags)

### Scraper
- Headless browser: faster than GUI
- Parallel processing: not implemented (add with asyncio)
- Rate limiting: wait 500ms between scrolls
- Timeout: 30s per post

To improve scraper speed:
```python
# Reduce timeouts (risky)
timeout=5000  # was 10000

# Reduce scroll waits
await page.wait_for_timeout(200)  # was 500

# Limit posts per run
for link in post_links[:10]:  # was 20
```

## Security Considerations

### Instagram Login
- Credentials via environment variables only
- Never hardcode in files
- GitHub Secrets are encrypted

### Image Downloads
- Validates URLs before download
- Saves locally only
- No external uploads

### Data Storage
- posts.json is public (on GitHub Pages)
- Remove sensitive data before committing
- No passwords/tokens in JSON

## Monitoring

### Check Status
```bash
# View last sync time
jq '.last_updated' data/posts.json

# Count posts by category
jq 'group_by(.category) | map({(.[0].category): length})' data/posts.json

# Find empty/broken posts
jq '.posts[] | select(.images | length == 0)' data/posts.json
```

### GitHub Actions
- Check Actions tab for run history
- View logs if workflow fails
- See what changed in each commit

### Logs
```bash
# View scraper logs
python scraper/scrape.py 2>&1 | tee scraper.log

# Follow logs (if running as service)
tail -f scraper.log
```

---

Need help? Check README.md or QUICKSTART.md
