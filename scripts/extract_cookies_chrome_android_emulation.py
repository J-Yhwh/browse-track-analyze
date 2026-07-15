from playwright.sync_api import sync_playwright
import csv
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path.home() / "Desktop" / "browse-track-analyze"
DATA_FOLDER = REPO_ROOT / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)

output_csv = DATA_FOLDER / "chrome_android_emulated_cookies.csv"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        viewport={"width": 393, "height": 851},
        device_scale_factor=3.0,
        is_mobile=True,
        has_touch=True,
        locale="en-AU",
        timezone_id="Asia/Singapore",
        extra_http_headers={"Sec-CH-UA-Platform": '"Android"'},
        bypass_csp=True,
        ignore_https_errors=True,
    )

    page = context.new_page()

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

    all_cookies = []

    for url in urls:
        try:
            print(f"🌐 Visiting: {url}")
            timeout = 90000 if "x.com" in url or "dailymail" in url else 60000
            page.goto(url, wait_until="networkidle", timeout=timeout)
            page.wait_for_timeout(4000)
            
            cookies = context.cookies()
            all_cookies.extend([c for c in cookies if isinstance(c, dict)])
            print(f"✅ Extracted {len(cookies)} cookies from {url}")
            
        except Exception as e:
            print(f"❌ Error visiting {url}: {e}")

    # Export to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'name', 'value', 'path', 'expires', 'secure', 'httpOnly', 'platform'])
        for cookie in all_cookies:
            writer.writerow([
                cookie.get("domain"),
                cookie.get("name"),
                cookie.get("value"),
                cookie.get("path"),
                cookie.get("expires", ""),
                cookie.get("secure", False),
                cookie.get("httpOnly", False),
                "Android Chrome (Playwright)"
            ])

print(f"✅ Exported {len(all_cookies)} cookies to {output_csv}")
browser.close()
