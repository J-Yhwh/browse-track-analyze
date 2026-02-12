
from playwright.sync_api import sync_playwright
import csv


output_csv = "brave_ios_emulated_cookies.csv"


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
    page.goto("https://www.youtube.com", "https://www.google.com", "https://", "", "")         # <- replace with real test URLs


    cookies = context.cookies()


    # Export to CSV
    with open(output_csv, 'w', newline='' , encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'name', 'value', 'path', 'expires', 'secure', 'httpOnly','platform'])
        for cookie in cookies:
            writer.writerow([
                cookie["domain"],
                cookie["name"],
                cookie["value"],
                cookie["path"],
                cookie["expires", ""],
                cookie["secure"],
                cookie["httpOnly"],
                "iOS Brave(Webkit emulation)"
            ])


    print(f"✅ Exported{len[cookies]} cookies to {output_csv}")
    browser.close()
