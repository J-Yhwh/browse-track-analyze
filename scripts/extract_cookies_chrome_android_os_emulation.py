
from playwright.sync_api import sync_playwright
import csv

from pathlib import Path
from datetime import datetime


# Maprepo/file root path for storing the extracted .csv file
REPO_ROOT = Path.home() / "Desktop" / "browse-track-analyze"
DATA_FOLDER = REPO_ROOT / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)  #creates the folder if missing

#file path of the generated csv file extraction of Chrome cookies
output_csv = DATA_FOLDER / "chrome_android_emulated_cookies.csv"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)      #headless=True later for automation


    context = browser.new_context(
        user_agent= "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        viewport={"width": 393, "height": 851},     #common Android phone size
        device_scale_factor=3.0,
        is_mobile=True,
        has_touch=True,
        locale= "en-AU",
        timezone_id="Asia/Singapore",
        extra_http_headers={"Sec-CH-UA-Platform": '"Android"'},
        ignore_https_errors=True,
    )


    page = context.new_page()


    #visit sites you want to test
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
            print(f"🌏 Visiting: {url}")

            
            if any(site in url for site in ["dailymail.co.uk", "x.com", "msn.com", "channelnewsasia.com"]):
                page.goto(url, wait_until="domcontentloaded", timeout=180000) # Allocated extra timeout for "heavy" news and sm sites
                page.wait_for_timeout(20000)
            else:
                page.goto(url, wait_until="networkidle", timeout=120000)       # Normal sites
                page.wait_for_timeout(9000)

                
            cookies = context.cookies()
            all_cookies.extend(cookies)
            print(f"✅ Extracted {len(cookies)} cookies from {url}")

        except Exception as e:
            print(f"❌ Error visiting{url}: {e}")



# Export to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['domain', 'name', 'value', 'path', 'expires', 'secure', 'httpOnly', 'platform'])
    for cookie in all_cookies:
        writer.writerow([
            cookie.get("domain", ""),
            cookie.get("name", ""),
            cookie.get("value", ""),
            cookie.get("path", ""),
            cookie.get("expires", ""),
            cookie.get("secure", False),
            cookie.get("httpOnly", False),
            "Android Chrome (Playwright)"
        ])

print(f"✅ Exported {len(all_cookies)} cookies to {output_csv}")


# Safe cleanup
try:
    context.close()
    browser.close()
except:
    pass

