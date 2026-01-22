import asyncio
import os
from playwright.async_api import async_playwright

# DEFINE USER INFO (from environment variables)
EMAIL = os.getenv("X_EMAIL", "your_email@example.com")
PASSWORD = os.getenv("X_PASSWORD", "your_password")
PROFILE_DIR = os.getenv("X_PROFILE_DIR", "test_profile")

# DEFINE BROWSER
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
LOCALE = "th-TH"
TIMEZONE = "Asia/Bangkok"
OPTIONS = [
    "--start-maximized",
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor"
]

async def check_login_status(context):
    """Check if user is logged in to X.com by checking cookies."""
    cookies = await context.cookies()
    # X/Twitter uses 'auth_token' as main authentication cookie
    is_logged_in = any(cookie['name'] == 'auth_token' for cookie in cookies)
    return is_logged_in

async def scrape_tweets(page, limit=3):
    """Scrape tweets from the current page."""
    try:
        # Wait for tweets to load
        print("Waiting for tweets to load...")
        await asyncio.sleep(2)

        # Use CSS selectors to find all tweet articles
        tweet_elements = await page.query_selector_all("article[data-testid='tweet']")

        tweet_count = len(tweet_elements)
        print(f"✓ Found {tweet_count} tweets on page")

        if tweet_count == 0:
            return []

        # Limit to specified number of tweets
        tweets_to_scrape = min(tweet_count, limit)
        print(f"Scraping first {tweets_to_scrape} tweets...")

        tweets = []
        for i in range(tweets_to_scrape):
            try:
                tweet_element = tweet_elements[i]

                # Extract tweet text (CSS selector)
                text_element = await tweet_element.query_selector("[data-testid='tweetText']")
                text = await text_element.inner_text() if text_element else "No text found"

                # Extract tweet author (CSS selector)
                author_element = await tweet_element.query_selector("[data-testid='User-Name']")
                author = await author_element.inner_text() if author_element else "Unknown author"

                # Extract timestamp/link (get the tweet status link)
                link_element = await tweet_element.query_selector("a[href*='/status/']")
                link = await link_element.get_attribute('href') if link_element else None
                tweet_url = f"https://x.com{link}" if link and not link.startswith('http') else link

                tweet_data = {
                    'index': i + 1,
                    'author': author.strip(),
                    'text': text.strip(),
                    'url': tweet_url if tweet_url else "No link"
                }
                tweets.append(tweet_data)

                print(f"  ✓ Tweet {i + 1} extracted")

            except Exception as e:
                print(f"  ✗ Error extracting tweet {i + 1}: {e}")
                continue

        return tweets

    except Exception as e:
        print(f"✗ Error scraping tweets: {e}")
        return []

async def get_profile_description(page, username):
    """Get the profile description/bio for a given username."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")

            # Go to profile page with longer timeout and domcontentloaded instead of networkidle
            await page.goto(
                f"https://x.com/{username}",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Wait for profile data to load - try to wait for specific elements
            try:
                # Wait for any profile-related element to appear
                await page.wait_for_selector('[data-testid="UserName"]', timeout=10000)
                print("✓ Profile elements detected")
            except:
                print("⚠ Profile selector not found, proceeding anyway...")

            await asyncio.sleep(3)

            # Try multiple selectors for profile description
            selectors = [
                'div[data-testid="UserDescription"]',  # Main bio selector
                '[data-testid="UserDescription"]',
                'div[data-testid="UserDescription"] span',  # Span inside bio
            ]

            description = None
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        description = await element.inner_text()
                        if description and description.strip():
                            print(f"✓ Found description with selector: {selector}")
                            break
                except:
                    continue

            if description:
                return description.strip()
            else:
                return "No description found"

        except Exception as e:
            print(f"✗ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
            else:
                return f"Error after {max_retries} attempts: {e}"

async def main():
    async with async_playwright() as p:
        # Launch persistent context
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            viewport={"width": 1366, "height": 768},
            user_agent=USER_AGENT,
            locale=LOCALE,
            timezone_id=TIMEZONE,
            args=OPTIONS
        )

        # Add stealth scripts
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        print(f"Browser version: {context.browser.version}")

        page = await context.new_page()

        # STEP 1: Go to https://x.com/NBA
        print("\n=== STEP 1: Navigating to https://x.com/NBA ===")
        try:
            await page.goto(
                "https://x.com/NBA",
                wait_until="domcontentloaded",
                timeout=60000
            )
            print("✓ Page loaded")
        except Exception as e:
            print(f"✗ Error loading page: {e}")
            print("Trying to continue anyway...")

        # STEP 2: Validate authentication
        print("\n=== STEP 2: Checking authentication status ===")
        is_logged_in = await check_login_status(context)

        if is_logged_in:
            print("✓ Already logged in to X.com (found auth_token cookie)")
        else:
            print("✗ Not logged in to X.com (no auth_token cookie)")
            # STEP 3: Login (just print for now)
            print("\n=== STEP 3: Login required ===")
            print("TODO: Implement login flow for X.com")
            print("Login steps would go here...")

        # STEP 4: Get profile description
        print("\n=== STEP 4: Getting profile description ===")
        description = await get_profile_description(page, "NBA")
        print(f"\nProfile Description for @NBA:")
        print(f"{'─' * 50}")
        print(f"{description}")
        print(f"{'─' * 50}")

        # STEP 5: Scrape tweets
        print("\n=== STEP 5: Scraping tweets ===")
        tweets = await scrape_tweets(page, limit=3)

        if tweets:
            print(f"\n{'=' * 70}")
            print(f"EXTRACTED TWEETS FROM @NBA")
            print(f"{'=' * 70}")
            for tweet in tweets:
                print(f"\nTWEET #{tweet['index']}")
                print(f"{'─' * 70}")
                print(f"Author: {tweet['author']}")
                print(f"Text: {tweet['text'][:200]}{'...' if len(tweet['text']) > 200 else ''}")
                print(f"URL: {tweet['url']}")
                print(f"{'─' * 70}")
        else:
            print("\n✗ No tweets found or unable to scrape tweets")

        # Keep browser open
        print("\n\nBrowser is ready. Press Enter to close...")
        input()
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
