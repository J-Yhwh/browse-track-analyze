
import sqlite3
import csv
import shutil
from pathlib import Path
from datetime import datetime



# ========================
# CONFIGURATION
# ========================

COOKIES_PATH = Path.home() / "Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies"
BACKUP_PATH = Path("cookies_backup.db")  # temporary copy in project folder
OUTPUT_CSV = Path("data/brave_macos_cookies.csv")

def extract_brave_cookies():
    """
    Safely extracts all cookies from Brave's SQLite database on macOS.
    Creates a temporary copy first to avoid lock errors.
    Outputs to CSV with human-readable dates.
    """
    if not COOKIES_PATH.exists():
        print(f"Error: Brave Cookies database not found at {COOKIES_PATH}")
        print("Make sure Brave is installed and has been used at least once.")
        return

    print("Creating temporary copy of Cookies database...")
    shutil.copy(COOKIES_PATH, BACKUP_PATH)

    try:
        conn = sqlite3.connect(BACKUP_PATH)
        cursor = conn.cursor()

        # Query all relevant cookie fields
        cursor.execute("""
            SELECT 
                host_key AS domain,
                name,
                value,
                path,
                expires_utc,
                is_secure,
                is_httponly,
                creation_utc
            FROM cookies
        """)

        rows = cursor.fetchall()

        # Write to CSV with readable timestamps
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'domain', 'name', 'value', 'path', 'expires_utc',
                'is_secure', 'is_httponly', 'creation_utc',
                'expires_date', 'creation_date'
            ])

            for row in rows:
                domain, name, value, path, expires_utc, secure, httponly, creation_utc = row

                # Convert microseconds (WebKit epoch) to readable dates
                # WebKit epoch starts from 1601-01-01 (11644473600 seconds offset)
                expires_date = "Never"
                creation_date = "Unknown"

                if expires_utc:
                    expires_unix = (expires_utc // 1000000) - 11644473600
                    expires_date = datetime.fromtimestamp(expires_unix).strftime('%Y-%m-%d %H:%M:%S')

                if creation_utc:
                    creation_unix = (creation_utc // 1000000) - 11644473600
                    creation_date = datetime.fromtimestamp(creation_unix).strftime('%Y-%m-%d %H:%M:%S')

                writer.writerow([
                    domain, name, value, path, expires_utc,
                    bool(secure), bool(httponly), creation_utc,
                    expires_date, creation_date
                ])

        print(f"Success! Exported {len(rows)} cookies to {OUTPUT_CSV}")

    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        print("Tip: Make sure Brave is fully closed (Cmd + Q) before running this script.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()
        # Clean up the temporary copy
        if BACKUP_PATH.exists():
            BACKUP_PATH.unlink()
            print("Temporary backup deleted.")

if __name__ == "__main__":
    extract_brave_cookies()
