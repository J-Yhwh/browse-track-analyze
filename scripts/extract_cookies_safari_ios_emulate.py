# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.


from playwright.sync_api import sync_playwright
import pandas as pd
from pathlib import Path
from datetime import datetime

# ================== CONFIG ==================
REPO_ROOT = Path.home() / "Desktop" / "main"
DATA_FOLDER = REPO_ROOT / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)

# ✅ Correct filename for Safari iOS
output_csv = DATA_FOLDER / "safari_ios_emulated_cookies.csv"


def scrape_safari_ios_cookies():
    all_cookies = []
    
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 390, "height": 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
            locale="en-AU",
            timezone_id="Asia/Singapore",
        )

        page = context.new_page()

        # Sites commonly used on mobile browsers (e.g Tiktok, Instagram,Youtube etc)
        urls = [
            "https://www.youtube.com",
            "https://www.google.com",
            "https://www.bing.com",
            "https://www.channelnewsasia.com",
            "https://www.dailymail.co.uk",
            "https://www.instagram.com",
            "https://www.msn.com",
            "https://www.tiktok.com",
            "https://www.x.com",
            "https://www.yahoo.com"
        ]

        # extracting all cookies from sites 
        for url in urls:
            try:
                print(f"🌐 Visiting: {url}")
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(4000)
                
                cookies = context.cookies()
                
                for cookie in cookies:
                    cookie["browser"] = "Safari"
                    cookie["os"] = "iOS (Playwright)"
                    cookie["url"] = url
                    cookie["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    all_cookies.append(cookie)
                
                print(f"✅ Extracted {len(cookies)} cookies from {url}")
                
            except Exception as e:
                print(f"❌ Error visiting {url}: {e}")

        context.close()
        browser.close()

    # ================== SAVE TO SINGLE MASTER CSV ==================
    if all_cookies:
        df = pd.DataFrame(all_cookies)
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"\n🎉 SUCCESS! Saved {len(all_cookies)} cookies to:")
        print(f"   {output_csv}")
    else:
        print("⚠️ No cookies were collected.")
        
if __name__ == "__main__":
    scrape_safari_ios_cookies()
