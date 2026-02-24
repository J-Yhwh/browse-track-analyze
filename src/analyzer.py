import sys
import os


#Librries required to generate the reporting analytics on cookie behaviour (for MacOS/iOS)
import argparse
import json
import pandas as pd
from pathlib import Path
from scripts.report import generate_report  # your report function


#Repo root designed to work exacly as categorized in project file-structure git
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, REPO_ROOT)


def main():
    parser = argparse.ArgumentParser(description="Browser Tracker Analyzer CLI")
    parser.add_argument("--mode", choices=["csv", "live"], default="csv",
                        help="csv: process existing CSVs | live: scrape new URL (future)")
    parser.add_argument("--output", default="browser_analysis",
                        help="Base name for output report files (no extension)")
    parser.add_argument("--format", default="json", choices=["json", "csv", "html"],
                        help="Report format")
    args = parser.parse_args()

    REPO_ROOT = Path.home() / "Desktop" / "main"
    DATA_FOLDER = REPO_ROOT / "data"

    if args.mode == "csv":
        # Load your two CSVs
        macos_path = DATA_FOLDER / "brave_macos_cookies.csv"
        ios_path   = DATA_FOLDER / "brave_ios_emulated_cookies.csv"

        if not macos_path.exists() or not ios_path.exists():
            print("Error: One or both CSVs missing in data/")
            return

        macos_df = pd.read_csv(macos_path)
        ios_df   = pd.read_csv(ios_path)

        # Add platform labels
        macos_df['platform'] = 'macOS'
        ios_df['platform']   = 'iOS'

        # Create three datasets
        macos_only = macos_df.copy()
        ios_only   = ios_df.copy()
        combined   = pd.concat([macos_df, ios_df], ignore_index=True)

        # Optional debug summaries (only show in normal mode, not -O)
        if __debug__:
            print("\n=== Summary ===")
            print("macOS only:", macos_only.shape)
            print(macos_only['domain'].value_counts().head(5))
            print("\niOS only:", ios_only.shape)
            print(ios_only['domain'].value_counts().head(5))
            print("\nCombined:", combined.shape)
            print(combined['domain'].value_counts().head(5))

        # Build three report data dicts
        macos_report = {
            "platform": "macOS",
            "cookies_count": len(macos_only),
            "unique_domains": macos_only['domain'].nunique(),
            "top_domains": macos_only['domain'].value_counts().head(10).to_dict(),
            "secure_ratio": macos_only['is_secure'].mean() if 'is_secure' in macos_only else 0,
            "http_only_ratio": macos_only['is_httponly'].mean() if 'is_httponly' in macos_only else 0,
            # Add more stats as you like
        }

        ios_report = {
            "platform": "iOS (emulated)",
            "cookies_count": len(ios_only),
            "unique_domains": ios_only['domain'].nunique(),
            "top_domains": ios_only['domain'].value_counts().head(10).to_dict(),
            "secure_ratio": ios_only['is_secure'].mean() if 'is_secure' in ios_only else 0,
            "http_only_ratio": ios_only['is_httponly'].mean() if 'is_httponly' in ios_only else 0,
        }

        combined_report = {
            "platforms": ["macOS", "iOS (emulated)"],
            "total_cookies": len(combined),
            "macos_cookies": len(macos_only),
            "ios_cookies": len(ios_only),
            "top_domains_overall": combined['domain'].value_counts().head(10).to_dict(),
            "macos_top_domains": macos_only['domain'].value_counts().head(5).to_dict(),
            "ios_top_domains": ios_only['domain'].value_counts().head(5).to_dict(),
            "secure_ratio_macos": macos_report["secure_ratio"],
            "secure_ratio_ios": ios_report["secure_ratio"],
            "http_only_ratio_macos": macos_report["http_only_ratio"],
            "http_only_ratio_ios": ios_report["http_only_ratio"],
            # Add more...
        }

        # Generate three separate reports
        generate_report(macos_report,     format=args.format, output=f"{args.output}_macos")
        generate_report(ios_report,       format=args.format, output=f"{args.output}_ios")
        generate_report(combined_report,  format=args.format, output=f"{args.output}_combined")

        print("\nAll three reports generated successfully!")

    elif args.mode == "live":
        print("Live scraping mode not implemented yet. Use --mode csv for now.")

if __name__ == "__main__":
    main()

    
