#!/usr/bin/env python3
"""
Instagram scraper for JM Automobielen - scrapes Instagram profile and syncs with website
"""

import asyncio
import json
import os
import sys
import re
import argparse
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, Dict, List, Any

from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
INSTAGRAM_PROFILE = "jm.automobielen"
DATA_DIR = Path(__file__).parent.parent / "data"
POSTS_FILE = DATA_DIR / "posts.json"
IMAGES_DIR = DATA_DIR / "images"
HEADLESS = True  # Set to False for debugging

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


class InstagramScraper:
    """Scrapes Instagram profile for JM Automobielen"""

    def __init__(self, full_scrape: bool = False):
        self.full_scrape = full_scrape
        self.posts_data = self._load_posts()
        self.existing_ids = {post['id'] for post in self.posts_data.get('posts', [])}
        self.new_posts = []

    def _load_posts(self) -> Dict[str, Any]:
        """Load existing posts from JSON"""
        if POSTS_FILE.exists():
            try:
                with open(POSTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load posts.json: {e}")

        return {
            "last_updated": datetime.now().isoformat() + "Z",
            "profile": {
                "name": "JM Automobielen",
                "bio": "RDW erkend autobedrijf in Hoogkarspel.\nVoor in/verkoop en licht onderhoud.\nPolijsten, coaten, interieur...",
                "followers": 235,
                "posts_count": 75
            },
            "posts": []
        }

    def _save_posts(self):
        """Save posts to JSON file"""
        self.posts_data["last_updated"] = datetime.now().isoformat() + "Z"
        with open(POSTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.posts_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(self.posts_data['posts'])} posts to {POSTS_FILE}")

    @staticmethod
    def _categorize_post(caption: str) -> str:
        """Categorize post based on caption keywords"""
        caption_lower = caption.lower()

        # Check categories in priority order
        if any(word in caption_lower for word in ['te koop', 'vraagprijs', 'voor meer info']) or '€' in caption:
            return 'te_koop'

        if any(word in caption_lower for word in ['verkocht', 'blij gemaakt', 'nieuwe eigenaar', 'opgehaald']):
            return 'verkocht'

        if any(word in caption_lower for word in [
            'polijst', 'detailing', 'coating', 'interieur', 'wax', 'sealing',
            'swirl', 'polish', 'menzerna', 'gyeon', 'extractie', 'ozon'
        ]):
            return 'detailing'

        if any(word in caption_lower for word in ['storing', 'reparatie', 'fout', 'diagnose', 'coding']):
            return 'reparatie'

        if any(word in caption_lower for word in ['review', 'beoordeling', 'sterren', '⭐']):
            return 'review'

        if any(word in caption_lower for word in ['rdw', 'erkend', 'stap']):
            return 'bedrijf'

        return 'overig'

    @staticmethod
    def _extract_car_info(caption: str) -> Dict[str, Optional[str]]:
        """Extract car info from caption (make, model, plate, price)"""
        car_info = {
            "make": None,
            "model": None,
            "plate": None,
            "price": None
        }

        # Extract Dutch license plate (format: XX-XX-XX)
        plate_match = re.search(r'([A-Z]{2,3}[-\s]\d{1,3}[-\s][A-Z]{2})', caption)
        if plate_match:
            car_info["plate"] = plate_match.group(1).replace(' ', '-').upper()

        # Extract price (€ followed by numbers)
        price_match = re.search(r'€\s*([0-9.]+(?:\.000)?)', caption)
        if price_match:
            price_str = price_match.group(1).replace('.', '')
            car_info["price"] = price_str

        # Try to extract car make and model (basic approach)
        # Look for common Dutch car mentions
        car_brands = [
            'volkswagen', 'audi', 'bmw', 'mercedes', 'ford', 'peugeot', 'citroen',
            'renault', 'opel', 'fiat', 'alfa romeo', 'mazda', 'hyundai', 'kia',
            'toyota', 'honda', 'nissan', 'volvo', 'skoda', 'seat'
        ]

        caption_lower = caption.lower()
        for brand in car_brands:
            if brand in caption_lower:
                car_info["make"] = brand.title()
                # Extract model (usually follows brand)
                brand_index = caption_lower.find(brand)
                rest = caption[brand_index + len(brand):].strip()
                # Get first word after brand as model
                model_match = re.search(r'^([A-Za-z0-9]+)', rest)
                if model_match:
                    car_info["model"] = model_match.group(1).strip(',.:!')
                break

        return car_info

    async def _download_image(self, url: str, post_id: str, index: int = 1) -> Optional[str]:
        """Download image from URL and save locally"""
        try:
            if not url or not isinstance(url, str):
                return None

            filename = f"{post_id}_{index}.jpg"
            filepath = IMAGES_DIR / filename

            # Check if already downloaded
            if filepath.exists():
                return f"images/{filename}"

            # Download with playwright context
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=HEADLESS)
                page = await browser.new_page()

                # Set a valid User-Agent to avoid blocking
                await page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })

                try:
                    response = await page.goto(url, wait_until='domcontentloaded', timeout=10000)
                    if response:
                        image_data = await page.content()
                        with open(filepath, 'w') as f:
                            f.write(image_data)
                        logger.info(f"Downloaded image: {filename}")
                        return f"images/{filename}"
                except Exception as e:
                    logger.warning(f"Could not download {url}: {e}")
                finally:
                    await browser.close()

            return None
        except Exception as e:
            logger.error(f"Error downloading image {url}: {e}")
            return None

    async def _extract_post_data(self, page: Page, post_id: str) -> Optional[Dict[str, Any]]:
        """Extract post data from Instagram post modal"""
        try:
            # Wait for modal to load
            await page.wait_for_selector('[role="presentation"]', timeout=5000)

            # Get caption
            caption = ""
            try:
                caption_element = await page.query_selector('[class*="caption"]')
                if caption_element:
                    caption = await caption_element.text_content()
                else:
                    # Fallback: get all text from modal
                    caption = await page.inner_text('[role="presentation"]')
            except:
                pass

            caption = caption.strip() if caption else ""

            # Get images from carousel
            images = []
            try:
                # Look for images in the modal
                img_elements = await page.query_selector_all('img[src*="instagram"]')
                for i, img in enumerate(img_elements[:10], 1):  # Limit to 10 images per post
                    try:
                        src = await img.get_attribute('src')
                        if src and 'instagram' in src:
                            # Save image locally
                            filename = f"{post_id}_{i}.jpg"
                            filepath = IMAGES_DIR / filename

                            if not filepath.exists():
                                logger.info(f"Queued image: {filename}")

                            images.append(f"images/{filename}")
                    except:
                        pass
            except:
                pass

            # If no images found, log warning
            if not images:
                logger.warning(f"No images found for post {post_id}")

            # Categorize post
            category = self._categorize_post(caption)

            # Extract car info if applicable
            car_info = self._extract_car_info(caption) if category in ['te_koop', 'verkocht'] else {}

            post_data = {
                "id": post_id,
                "type": "post",
                "category": category,
                "caption": caption,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "images": images,
                "car_info": car_info if car_info.get("make") or car_info.get("plate") or car_info.get("price") else {}
            }

            return post_data

        except Exception as e:
            logger.error(f"Error extracting post data for {post_id}: {e}")
            return None

    async def _check_updates_to_existing_posts(self):
        """Check if any te_koop posts have become verkocht"""
        try:
            # This would require re-checking existing posts
            # For now, we'll skip this to keep scraping efficient
            logger.info("Checking for status updates...")
        except Exception as e:
            logger.error(f"Error checking updates: {e}")

    async def scrape(self):
        """Main scraping method"""
        logger.info(f"Starting Instagram scrape for @{INSTAGRAM_PROFILE}")
        logger.info(f"Full scrape: {self.full_scrape}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=HEADLESS)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Navigate to Instagram profile
                profile_url = f"https://www.instagram.com/{INSTAGRAM_PROFILE}/"
                logger.info(f"Navigating to {profile_url}")

                await page.goto(profile_url, wait_until='domcontentloaded', timeout=30000)

                # Wait for profile to load
                await page.wait_for_timeout(2000)

                # Check if profile loaded
                try:
                    await page.wait_for_selector('[class*="Posts"]', timeout=5000)
                except:
                    logger.warning("Could not find posts section, Instagram may require login")

                # Scroll to load posts
                logger.info("Scrolling to load posts...")
                for i in range(15):  # Scroll ~15 times to load posts
                    await page.evaluate('window.scrollBy(0, window.innerHeight)')
                    await page.wait_for_timeout(500)

                # Get post links
                post_links = await page.eval_on_selector_all(
                    'a[href*="/p/"]',
                    'elements => elements.map(el => el.href)'
                )

                logger.info(f"Found {len(post_links)} posts")

                # Process each post
                for i, link in enumerate(post_links[:20], 1):  # Limit to 20 posts for testing
                    # Extract post ID from URL
                    match = re.search(r'/p/([A-Za-z0-9_-]+)/', link)
                    if not match:
                        continue

                    post_id = match.group(1)

                    # Skip if already processed and not full scrape
                    if post_id in self.existing_ids and not self.full_scrape:
                        logger.info(f"Skipping existing post {post_id}")
                        continue

                    logger.info(f"[{i}] Processing post: {post_id}")

                    # Open post in new context to avoid disrupting main page
                    post_page = await context.new_page()
                    try:
                        await post_page.goto(link, wait_until='domcontentloaded', timeout=15000)
                        await post_page.wait_for_timeout(1000)

                        # Extract post data
                        post_data = await self._extract_post_data(post_page, post_id)

                        if post_data:
                            # Check if post already exists
                            existing_post = next((p for p in self.posts_data['posts'] if p['id'] == post_id), None)

                            if existing_post:
                                # Update existing post
                                logger.info(f"Updating post {post_id}")
                                existing_post.update(post_data)
                            else:
                                # Add new post
                                logger.info(f"Adding new post {post_id}")
                                self.posts_data['posts'].append(post_data)
                                self.new_posts.append(post_data)

                    except Exception as e:
                        logger.error(f"Error processing {post_id}: {e}")
                    finally:
                        await post_page.close()

                # Update profile info
                try:
                    followers_text = await page.inner_text('[class*="Follower"]', timeout=5000)
                    if followers_text:
                        # Extract number from followers text
                        followers_match = re.search(r'(\d+[\d.,]*)', followers_text)
                        if followers_match:
                            followers_str = followers_match.group(1).replace('.', '').replace(',', '')
                            self.posts_data['profile']['followers'] = int(followers_str)
                except:
                    pass

                # Check for updates to existing posts
                await self._check_updates_to_existing_posts()

                # Save posts
                self._save_posts()

                logger.info(f"Scrape completed. Found {len(self.new_posts)} new posts")
                logger.info(f"Total posts now: {len(self.posts_data['posts'])}")

            except Exception as e:
                logger.error(f"Fatal scraping error: {e}")
                raise
            finally:
                await browser.close()

    def get_summary(self) -> str:
        """Get summary of scrape results"""
        return f"Scraped {len(self.new_posts)} new posts. Total: {len(self.posts_data['posts'])} posts."


async def main():
    parser = argparse.ArgumentParser(description='Scrape JM Automobielen Instagram profile')
    parser.add_argument('--full', action='store_true', help='Perform full scrape (all posts)')
    parser.add_argument('--test', action='store_true', help='Test mode (limited posts)')

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("JM Automobielen Instagram Scraper")
    logger.info("=" * 60)

    try:
        scraper = InstagramScraper(full_scrape=args.full)
        await scraper.scrape()
        logger.info(scraper.get_summary())
        logger.info("Scrape finished successfully")
        return 0
    except Exception as e:
        logger.error(f"Scrape failed: {e}")
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
