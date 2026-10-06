# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.

import pandas as pd
import sys

from datetime import datetime
from playwright.sync_api import sync_playwright
from pathlib import Path



# ==================================== CONFIG =====================================

# Mapping  root path to store extracted .csv files (Path Library of pathlib)

REPO_ROOT = Path.home() / "Desktop" / "browse-track-analyze" 
DATA_FOLDER = REPO_ROOT / "data" 
DATA_FOLDER.mkdir(exist_ok=True, parents=True)


# ✅ CSV file outputs of the differnt browsers running on iOS

OUTPUTS = {
    "Safari": DATA_FOLDER / "safari_ios_emulated_cookies.csv",
    "Brave" :  DATA_FOLDER / "brave_ios_emulated_cookies.csv",
    "Chrome": DATA_FOLDER / "chrome_ios_emulated_cookies.csv",
    "Firefox": DATA_FOLDER / "firefox_ios_emulated_cookies.csv",
}


# AppleWebkit engines for external (non-native) Browsers running in iOS

BRAVE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
)


CHROME_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "CriOS/131.0.6778.73 Mobile/15E148 Safari/604.1"
)


FIREFOX_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "FxiOS/132.0 Mobile/15E148 Safari 604.1"
    
)



PROFILES = [
    {"name": "Safari", "ua": None},
    {"name": "Brave", "ua": BRAVE_UA},
    {"name": "Firefox", "ua": FIREFOX_UA},
    {"name": "Chrome", "ua": CHROME_UA},
]


URLS = [
         "https://youtube.com",
         "https://www.google.com",
         "https://www.bing.com",
         "https://www.channelnewsasia.com",
         "https://www.dailymail.co.uk",
         "https://www.foxnews.com",
         "https://www.msn.com",
         "https://www.tiktok.com",
         "https://www.x.com",
         "https://www.yahoo.com"
]


SHOW_BROWSER = True    #Boolean switch to False if silent run (no pop-up of Playwirght simulation) is preferred

with sync_playwright() as p:
    browser = p.webkit.launch(
        headless=not SHOW_BROWSER,
        slow_mo=400 if SHOW_BROWSER else 0,
    )
    device = p.devices["iPhone 15"]


    for profile in PROFILES:
        rows = []    #one list per browser, created before any append
        kwargs = dict(device)
        if profile["ua"]:
            kwargs["user_agent"] = profile["ua"]
        context = browser.new_context(**kwargs)
        page = context.new_page()
    

        for url in URLS:
            try:
                print(f"visiting {url} [{profile['name']}]")
                page.goto(url, wait_until= "domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)
                cookies = context.cookies()
                for cookie in context.cookies():
                    expires_at = cookie.get("expires", -1)
                    rows.append({
                        "browser": profile["name"],
                        "os": "iOS(Playwright)", 
                        "url": url,
                        "domain": cookie.get("domain", ""),
                        "name": cookie.get("name", ""),
                        "path": cookie.get("path", ""),
                        "expires": "Yes" if expires_at and expires_at > 0 else "No",
                        "secure": cookie.get("secure", False),
                        "httpOnly": cookie.get("httpOnly", False),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
            except Exception as e:
                    print(f"error {url}: {e}")

                    
        context.close()
        out = OUTPUTS[profile["name"]]
        pd.DataFrame(rows).to_csv(out, index=False)
        print(f"wrote {len(rows)} rows -> {out}")


        
    browser.close()
            

                
            
       
        
         
        
            
            
