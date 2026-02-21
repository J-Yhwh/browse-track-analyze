

from playwright.sync_api import sync_playwright

import sqlite3
import csv
import shutil
from pathlib import Path
from datetime import datetime


#Map your repo/file root path for storing the extracted .csv file
REPO_ROOT = Path.home() / "Desktop" / "main"
DATA_FOLDER = REPO_ROOT / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)  #creates the folder if missing

#file path of the generated csv file extraction of cookies from iOS (Brave Browser) 
output_csv = DATA_FOLDER / "brave_ios_emulated_cookies.csv"


with sync_playwright() as p:
    #Webkit = Real iOS Safari/ Brave engine (Mobile Brave browser-engines are Safari-based, as opposed to Desktop Brave on  MacOS)
    browser = p.webkit.launch(headless=False)      #headless=True later for automatino


    context = browser.new_context(
        user_agent= "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        viewport={"width": 390, "height": 844},     #standard size of iPhone 14/15
        device_scale_factor=3.0,
        is_mobile=True,
        has_touch=True,
        locale= "en-AU",
        timezone_id="Asia/Singapore",
        extra_http_headers={"Sec-CH-UA-Platform": '"iOS"'},
        bypass_csp=True,
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

    #extract all cookies from sites         
    for url in urls:
        page.goto(url)
        # Optional: add assertions, screenshots, or cookie collection here
        cookies = context.cookies()
        all_cookies.extend(cookies)
        print(f"Cookies from {url}: {cookies}")



# Export to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['domain', 'name', 'value', 'path', 'expires', 'secure', 'httpOnly', 'platform'])
    for cookie in all_cookies:
        writer.writerow([
            cookie["domain"],
            cookie["name"],
            cookie["value"],
            cookie["path"],
            cookie.get("expires", ""),  # Safe access
            cookie["secure"],
            cookie["httpOnly"],
            "iOS Brave(Webkit emulation)"
        ])

print(f"✅ Exported {len(all_cookies)} cookies to {output_csv}")
browser.close()
