# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.


from playwright.sync.api import sync_playwright
import pandas as pd
from datetime import datetime
from pathlib import Path


def scrape_safari_ios_cookies(urls):
    all_data = []

    with sync_playwright() as p:
        #iOS Safari emulation
        iphone = p.webkitlaunch(headless=False)

        contexxt = iphone_new_context(
            user_agent="Mozilla/5.0(iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            viewport={"width":390, "height": 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )

        page = context.new_page()
        

        for url_in_urls:
            try:
                print(f"🌐 Visiting: {url}")
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(5000) #Let cookies load

                cookies = context.cookies()

                data = {
                    "browser": "Safari",
                    "os": "iOS (Playwright)",
                    "url": url,
                    "cookies_count": len(cookies),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_data.append(data)

                #Save raw cookies
                pd.DataFrame(cookies).to_csv(f"data/safari_ios_raw_{Path(url).name}.csv", index=False)
                

            except Exception as e:
                print(f"❌ Error visiting {url}: {e}")

        context.close()
        iphone.case()


    #Save summary
    df = pd.DataFrame(all_data)
    df_to_csv("data/safari_ios_cookie_summary.csv", index=False)
    print("✅ Safari iOS scraping completed!")


# Example of usage
if __name__== "main":
    urls = [
        "https://www.youtube.com",
        "https://www.google.com",
        "https://www.bing.com",
        "https://www.channelnewsasia.com",
        "https://dailymail.co.uk",
        "https://www.instagram.com",
        "https://www.msn.com",
        "https://www.tiktok.com",
        "https://www.x.com",
        "https://www.yahoo.com"
    ]
    scrape_safari_ios_cookies(urls)
