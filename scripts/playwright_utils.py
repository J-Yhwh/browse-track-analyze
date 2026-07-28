



from playwright.sync_api import sync_playwright
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_FOLDER = Path.home() / "Desktop" / "browse-track-analyze" / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)


def scrape_cookies_playwright(browser_type="webkit", urls=None, output_name=None):
    """
    browser_type options:
    - "webkit"      → Safari (macOS + iOS emulation)
    - "edge" / "msedge" → Microsoft Edge
    - "chromium"    → Chrome / Brave Desktop
    - "firefox"     → Firefox
    """
    if urls is None:
        urls = ["https://www.google.com", "https://www.youtube.com"]

    if output_name is None:
        output_name = f"{browser_type}_cookies.csv"

    all_cookies = []

    with sync_playwright() as p:
        if browser_type.lower() == "webkit":
            browser = p.webkit.launch(headless=False)
            os_name = "Safari (WebKit)"
        elif browser_type.lower() in ["edge", "msedge"]:
            browser = p.chromium.launch(channel="msedge", headless=False)
            os_name = "Windows (Edge)"
        elif browser_type.lower() in ["chromium", "chrome", "brave"]:
            browser = p.chromium.launch(headless=False)
            os_name = "Desktop (Chromium)"
        else:
            browser = p.firefox.launch(headless=False)
            os_name = "Desktop (Firefox)"

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Visiting: {url}")
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(4000)

                cookies = context.cookies()

                for cookie in cookies:
                    cookie["browser"] = browser_type.capitalize()
                    cookie["os"] = os_name
                    cookie["url"] = url
                    cookie["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    all_cookies.append(cookie)

                print(f"✅ Extracted {len(cookies)} cookies from {url}")

            except Exception as e:
                print(f"❌ Error on {url}: {e}")

        context.close()
        browser.close()

    if all_cookies:
        df = pd.DataFrame(all_cookies)
        output_path = DATA_FOLDER / output_name
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"🎉 Saved {len(all_cookies)} cookies to: {output_path}")
    else:
        print("⚠️ No cookies were collected.")


if __name__ == "__main__":
    # Test Safari
    scrape_cookies_playwright(browser_type="webkit", output_name="safari_cookies.csv")
