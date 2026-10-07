# Copyright (c) 2026. Jac LL
# ALL Rights Reserved.
# All unauthorized use or distribution is prohibited.


import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright
from pathlib import Path




#===================CONFIG - Directory Folders  & CSV File Paths ====================

REPO_ROOT = Path.home() / "Desktop" / "browse-track-analyze"
DATA_FOLDER = REPO_ROOT
DATA_FOLDER.mkdir(exist_ok = True, parents=True)


OUTPUTS = {
    "Chrome": DATA_FOLDER / "data"/ "chrome_android_emulated_cookies.csv",
    "Brave": DATA_FOLDER / "data"/  "brave_android_emulated_cookies.csv",
    "Firefox": DATA_FOLDER / "data"/ "firefox_android_emulated_cookies.csv",
    "Edge": DATA_FOLDER / "data"/ "edge_android_emulated_cookies.csv",
}


CHROME_UA = (
    "Mozilla/5.0(Linux; Android 14; Pixel 7) AppleAebKit/537.36"
    "(KHTML, like Gecko)  Chrome/131.0.6778.135 Mobile Safari/537.36"
)
BRAVE_UA = (
    "Mozilla/5.0(Linux; Android 14; Pixel 7) AppleAebKit/537.36"
    "(KHTML, like Gecko)  Chrome/131.0.6778.135 Mobile Safari/537.36"
)
FIREFOX_UA = (
    "Mozilla/5.0(Linux; Android 14; Mobile; rv:132.0) Gecko/132.0  Firefox/132.0"
)
EDGE_UA = (
    "Mozilla/5.0(Linux; Android 14; Pixel 7) AppleAebKit/537.36"
    "(KHTML, like Gecko)  Chrome/131.0.6778.135 Mobile Safari/537.36 EdgA/131.0.2903.70"
)



PROFILES = [
    {"name": "Chrome", "ua": CHROME_UA},
    {"name":"Brave", "ua": BRAVE_UA},
    {"name":"Firefox", "ua": FIREFOX_UA},
    {"name":"Edge", "ua": EDGE_UA},
]


URLS = [
    "https://www.youtube.com",
    "https://www.google.com",
    "https://bing.com",
    "https://www.channelnewsasia.com",
    "https://dailymail.co.uk",
    "https://foxnews.com",
    "https://msn.com",
    "https://www.tiktok.com",
    "https://www.x.com",
    "https://www.yahoo.com",
]


SHOW_BROWSER = True


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=not SHOW_BROWSER,
        slow_mo=400 if SHOW_BROWSER else 0,
    )
    device = p.devices["Pixel 7"]


    for profile in PROFILES:
        rows = []
        kwargs = dict(device)
        kwargs["user_agent"] = profile["ua"]
        context = browser.new_context(**kwargs)
        page = context.new_page()

        for url in URLS:
            try:
                print(f"visiting {url} [{profile['name']}]")
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)
                for cookie in context.cookies():
                    expires_at = cookie.get("expires", -1)
                    rows.append({
                        "browser": profile["name"],
                        "os": "Android(Playwright)",
                        "url": url,
                        "domain": cookie.get("domain", ""),
                        "name": cookie.get("name", ""),
                        "path": cookie.get("path", ""),
                        "expires": "Yes" if expires_at and expires_at > 0 else "No",
                        "secure": cookie.get("secure", False),
                        "httpOnly": cookie.get("httpOnly", False),
                        "timestamp": datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),
                })
            except Exception as e:
                print(f"error {url}: {e}")

        context.close()
        out = OUTPUTS[profile["name"]]
        pd.DataFrame(rows).to_csv(out, index=False)
        print(f"wrote {len} rows -> {out}")

    browser.close()
                
    
            


    
