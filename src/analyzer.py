# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.

import sys
import os

#Libraries required to generate the reporting analytics on cookie behaviour (for MacOS/iOS)
import argparse
import json
import pandas as pd
import logging
from pathlib import Path
from scripts.report import generate_report  # your report function


# Repo root designed to work exactly as categorized in project file-structure git
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, REPO_ROOT)

# Setup logging envirornment
logging.basicConfig(
    filename= 'pipeline_integrity.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S'
)

# Define and set schema for data-cleansing
def verify_sanitize_schema(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    EXPECTED_SCHEMA = {
    'domain': 'string',
    'name': 'string',
    'value': 'string',
    'path': 'string',
    'secure': 'boolean',
    'httpOnly': 'boolean',
    'expiry': 'Int64'
    }

    logging.info(f"Initiating schema verfification for batch source:  [{source_name}]")
    
    # Check for missing critical columns
    missing_cols = [col for col in EXPECTED_SCHEMA if col not in df.columns]
    if missing_cols:
        error_msg = f"SCHEMA CRITICAL ERROR: Source [{source_name}] is missing required columns: {missing_cols}"
        logging.error(error_msg)
        for col in missing_cols:
            df[col] = pd.NA

        for column, target_type in EXPECTED_SCHEMA.items():
        if column in df.columns:
            try:
                initial_nulls = df[column].isna().sum()

                if target_type == "boolean":
                    df[column] = df[column].astype(bool)
                elif target_type == "Int64":
                    df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
                else:
                    df[column] = df[column].astype(target_type)

                final_nulls = df[column].isna().sum()
                if final_nulls > initial_nulls:
                    logging.warning(
                        f"Data anomaly in [{source_name}] column [{column}]. "
                        f"{final_nulls - initial_nulls} records failed type coercion and were set to NULL."
                    )
            except Exception as e:
                logging.error(
                    f"Failed to enforce type [{target_type}] on column [{column}] "
                    f"for [{source_name}]: {e}"
                )

    # Filter to strictly match the institutional format
    sanitized_df = df[list(EXPECTED_SCHEMA.keys())].copy()
    logging.info(f"Schema verification complete for [{source_name}]. Processed rows: {len(sanitized_df)}")
    return sanitized_df


# Transformation of raw data to readable CSV tables by parsing  
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

    
