#!/usr/bin/env python3
"""
Instagram scraper for JM Automobielen
Lightweight HTTP-based scraper (no browser needed).
Fetches public Instagram profile and post pages via meta tags.
"""

import json
import os
import re
import sys
import time
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

PROFILE = "jm.automobielen"
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"
POSTS_FILE = DATA_DIR / "posts.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}

DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


def fetch(url, retries=2):
    """Fetch a URL with retries and proper headers."""
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (URLError, HTTPError) as e:
            log.warning(f"Fetch attempt {attempt+1} failed for {url}: {e}")
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    return None


def fetch_bytes(url, retries=2):
    """Fetch binary content (images)."""
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=15) as resp:
                return resp.read()
        except (URLError, HTTPError) as e:
            log.warning(f"Image fetch attempt {attempt+1} failed: {e}")
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    return None


def extract_meta(html, prop):
    """Extract content from a meta tag."""
    pattern = rf'<meta\s+(?:property|name)="{re.escape(prop)}"\s+content="([^"]*)"'
    m = re.search(pattern, html, re.IGNORECASE)
    if m:
        return m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#039;", "'").replace("&quot;", '"')
    # Try reversed attribute order
    pattern2 = rf'<meta\s+content="([^"]*)"\s+(?:property|name)="{re.escape(prop)}"'
    m2 = re.search(pattern2, html, re.IGNORECASE)
    return m2.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#039;", "'").replace("&quot;", '"') if m2 else None


def parse_caption_from_og(og_desc):
    """Parse the real caption from Instagram's og:description format.
    Format: 'N likes, N comments - username on Date: "actual caption"'
    """
    if not og_desc:
        return ""
    m = re.search(r':\s*"(.+)"\.?\s*$', og_desc, re.DOTALL)
    return m.group(1).strip() if m else og_desc


def parse_date_from_og(og_desc):
    """Extract date from og:description. Format: '... on Month DD, YYYY: ...'"""
    if not og_desc:
        return None
    m = re.search(r'on\s+(\w+\s+\d{1,2},\s+\d{4})', og_desc)
    if m:
        try:
            from datetime import datetime as dt
            return dt.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def categorize(caption):
    """Auto-categorize post based on Dutch keywords in caption."""
    c = caption.lower()

    # Te koop indicators
    if any(w in c for w in ['te koop', 'vraagprijs', 'consignatie']) or re.search(r'€\s*\d', c):
        return 'te_koop'

    # Verkocht indicators
    if any(w in c for w in ['verkocht', 'afleveren', 'opgehaald', 'pad verlaten',
                             'eerste verkoop', 'blij gemaakt', 'nieuwe eigenaar',
                             'veilige kilometers', 'plezier ermee']):
        return 'verkocht'

    # Detailing indicators
    if any(w in c for w in ['polijst', 'detailing', 'coating', 'interieur behandeling',
                             'wax', 'sealing', 'swirl', 'polish', 'menzerna', 'ozon',
                             'schoonmaak', 'stofzuig', 'ramen', 'lampen', 'klei',
                             'extractie', 'reinig', 'schone']):
        return 'detailing'

    # Reparatie
    if any(w in c for w in ['reparatie', 'storing', 'diagnose', 'op de brug', 'onderhoud']):
        return 'reparatie'

    # Review
    if any(w in c for w in ['review', 'beoordeling', 'tevreden klant', '⭐']):
        return 'review'

    # Bedrijf
    if any(w in c for w in ['nieuwe spullen', 'rdw erkend', 'bedrijf', 'milestone']):
        return 'bedrijf'

    return 'overig'


def extract_car_info(caption):
    """Extract car make, model, price, km from caption."""
    info = {}
    c = caption.lower()

    brands = {
        'volkswagen': ['polo', 'golf', 'lupo', 'fox', 'up', 'passat', 'tiguan', 'transporter'],
        'audi': ['a1', 'a3', 'a4', 'a5', 'a6', 'rs3', 'rs4', 'q3', 'q5', 'tt'],
        'bmw': ['1', '2', '3', '4', '5', 'x1', 'x3', 'x5'],
        'ford': ['fiesta', 'focus', 'ka', 'puma', 'kuga'],
        'peugeot': ['106', '107', '108', '206', '207', '208', '306', '307', '308', '2008', '3008'],
        'renault': ['twingo', 'clio', 'megane', 'scenic', 'captur'],
        'opel': ['corsa', 'astra', 'karl', 'mokka'],
        'seat': ['ibiza', 'leon', 'arona', 'ateca'],
        'fiat': ['500', 'punto', 'panda'],
        'toyota': ['aygo', 'yaris', 'corolla', 'rav4'],
        'citroen': ['c1', 'c3', 'c4', 'berlingo'],
        'hyundai': ['i10', 'i20', 'i30', 'tucson'],
        'kia': ['picanto', 'rio', 'ceed', 'sportage'],
        'skoda': ['fabia', 'octavia', 'citigo'],
        'mazda': ['2', '3', 'cx-3', 'cx-5', 'mx-5'],
        'dacia': ['sandero', 'duster', 'logan'],
        'mini': ['cooper', 'one', 'clubman'],
        'suzuki': ['swift', 'alto', 'vitara'],
    }

    for brand, models in brands.items():
        if brand in c:
            info['make'] = brand.title()
            for model in models:
                if model in c:
                    info['model'] = model.title()
                    break
            if 'model' not in info:
                # Try to get word after brand
                idx = c.find(brand)
                rest = caption[idx + len(brand):].strip()
                m = re.match(r'(\w+)', rest)
                if m and len(m.group(1)) > 1:
                    info['model'] = m.group(1).strip(',.:!)')
            break

    # Also check for short brand names
    for short, full in [('vw', 'Volkswagen')]:
        if re.search(rf'\b{short}\b', c):
            info['make'] = full
            break

    # Price
    price_m = re.search(r'€\s*([\d.,]+)', caption)
    if price_m:
        price_str = price_m.group(1).replace('.', '').replace(',', '')
        try:
            info['price_eur'] = int(price_str)
        except ValueError:
            pass

    # KM
    km_m = re.search(r'([\d.]+)\s*(?:km|kilometer)', c)
    if km_m:
        km_str = km_m.group(1).replace('.', '')
        try:
            info['km'] = int(km_str)
        except ValueError:
            pass

    # Year
    year_m = re.search(r'\b(20[0-2]\d)\b', caption)
    if year_m:
        info['year'] = int(year_m.group(1))

    return info if info else None


def download_image(url, post_id):
    """Download image and save to data/images/. Returns local path or None."""
    if not url:
        return None

    ext = "jpg"
    filename = f"{post_id}.{ext}"
    filepath = IMAGES_DIR / filename

    if filepath.exists() and filepath.stat().st_size > 1000:
        log.info(f"Image already exists: {filename}")
        return f"data/images/{filename}"

    data = fetch_bytes(url)
    if data and len(data) > 1000:
        with open(filepath, 'wb') as f:
            f.write(data)
        log.info(f"Downloaded image: {filename} ({len(data)} bytes)")
        return f"data/images/{filename}"

    log.warning(f"Could not download image for {post_id}")
    return None


def load_posts():
    """Load existing posts.json."""
    if POSTS_FILE.exists():
        try:
            with open(POSTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log.warning(f"Could not load posts.json: {e}")
    return {"last_updated": None, "profile": {}, "posts": []}


def save_posts(data):
    """Save posts.json."""
    data["last_updated"] = datetime.now().isoformat() + "Z"
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info(f"Saved {len(data['posts'])} posts")


def scrape_profile():
    """Scrape the Instagram profile page for post URLs."""
    url = f"https://www.instagram.com/{PROFILE}/"
    html = fetch(url)
    if not html:
        log.error("Could not fetch profile page")
        return []

    # Extract post links from HTML
    post_ids = re.findall(r'/p/([A-Za-z0-9_-]+)/', html)
    unique_ids = list(dict.fromkeys(post_ids))  # deduplicate, preserve order
    log.info(f"Found {len(unique_ids)} post IDs on profile page")
    return unique_ids


def scrape_post(post_id):
    """Scrape a single post page for caption, date, and image."""
    url = f"https://www.instagram.com/p/{post_id}/"
    html = fetch(url)
    if not html:
        return None

    og_desc = extract_meta(html, "og:description")
    og_image = extract_meta(html, "og:image")

    caption = parse_caption_from_og(og_desc)
    date = parse_date_from_og(og_desc)
    category = categorize(caption)
    car_info = extract_car_info(caption) if category in ('te_koop', 'verkocht') else None

    # Download image
    local_image = download_image(og_image, post_id)

    post = {
        "id": post_id,
        "type": "post",
        "category": category,
        "caption": caption,
        "date": date,
        "image_url": f"https://www.instagram.com/p/{post_id}/media/?size=l",
    }

    if local_image:
        post["local_image"] = local_image

    if car_info:
        post["car_info"] = car_info

    return post


def main():
    log.info("=" * 50)
    log.info(f"JM Automobielen Instagram Scraper")
    log.info(f"Profile: @{PROFILE}")
    log.info("=" * 50)

    data = load_posts()
    existing_ids = {p['id'] for p in data.get('posts', [])}

    # Step 1: Get post IDs from profile
    post_ids = scrape_profile()

    if not post_ids:
        log.warning("No posts found on profile page. Instagram may be blocking requests.")
        log.info("Keeping existing data unchanged.")
        return 0

    # Step 2: Scrape new posts
    new_count = 0
    for pid in post_ids:
        if pid in existing_ids:
            log.info(f"Skipping existing post: {pid}")
            # Still try to download image if missing
            existing_post = next((p for p in data['posts'] if p['id'] == pid), None)
            if existing_post and not existing_post.get('local_image'):
                img = download_image(existing_post.get('image_url'), pid)
                if img:
                    existing_post['local_image'] = img
            continue

        log.info(f"Scraping new post: {pid}")
        post = scrape_post(pid)
        if post:
            data['posts'].insert(0, post)  # newest first
            new_count += 1
            log.info(f"  -> {post['category']}: {post['caption'][:80]}...")
        else:
            log.warning(f"  -> Could not scrape post {pid}")

        time.sleep(1)  # be polite

    # Step 3: Update profile info
    data['profile'] = {
        "name": "JM Automobielen",
        "bio": "RDW erkend autobedrijf in Hoogkarspel. Voor in/verkoop en licht onderhoud. Polijsten, coaten, interieur...",
        "instagram": f"https://www.instagram.com/{PROFILE}/",
    }

    # Step 4: Save
    save_posts(data)

    log.info(f"Done! {new_count} new posts. Total: {len(data['posts'])} posts.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
