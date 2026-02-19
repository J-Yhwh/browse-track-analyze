
# =========================================================
## CLI for parsing at Terminal(MacOS) or CMD (Windows) run
# =========================================================


import argparse
from pathlit import Path

from playwright.sync_api import sync_playwright
from trackers import is_tracker_url, categorize_tracker
from fingerprint import collect_fingerprint
from report import generate_report
 
##Optional:  add cookies/ storage analysis
from utils import analyze_cookies_and_storage  # if your system or OS has this feature 


def main():
    parser = argparse.ArgumentParser(description="Browser Tracker Analyzer")
    parser.add_argument("--url", required=True, help="URL to analyze")
    parser.add_argument("--output", default="report", help="Output file base name")
    parser.add_argument("--format", default="json", choices=["json", "csv", "html"])
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    output_path = Path(args.output)
 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(args.url, wait_until="networkidle", timeout=60000))
 
        # Collect data
        trackers = []
        for request in page.context.requests:
            if is_tracker_url(request.url):
                cat = categorize_tracker(request.url)
                trackers.append({"url": request.url, "category": cat})
 
        cookies_storage = analyze_cookies_and_storage(page)
        fp_data = collect_fingerprint(page)
 
        report = {
            "url": args.url,
            "trackers": trackers,
            "cookies_and_storage": cookies_storage,
            "fingerprint": fp_data,
        }
 
        ## Generate report
        generate_report(report, args.format, args.output)


        if args.verbose:
            print("Analysis complete. Report saved as {output_path}.{args.format}")
 
        browser.close()


 
if __name__ == "__main__":
    main()
