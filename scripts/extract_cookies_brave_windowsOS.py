import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# Correct path to Brave Cookies on Windows
cookie_db_path = Path(r"C:\FILEPATH\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies")

# Use your actual Desktop (OneDrive)
desktop = Path(r"C:\FILEPATH\OneDrive\Desktop")

if not cookie_db_path.exists():
    print("❌ Could not find Brave Cookies database.")
    print(f"   Expected path: {cookie_db_path}")
else:
    print(f"✅ Found Brave Cookies database!")

    conn = sqlite3.connect(cookie_db_path)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT 
        host_key as domain,
        name,
        value,
        path,
        expires_utc,
        is_secure as secure,
        is_httponly as httpOnly,
        creation_utc as creation_time
    FROM cookies
    ORDER BY host_key, name
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['browser'] = "Brave"

    # Save files to your actual Desktop
    raw_file = desktop / "brave_cookies_windows_raw.csv"
    df.to_csv(raw_file, index=False,encoding="utf-8")

    df.to_csv(raw_file, index=False, encoding="utf-8")

    # Simple summary
    summary = df.groupby('domain').size().reset_index(name='cookies_count')
    summary.to_csv(raw_file, index=False, encoding="utf-8")

    print(f"✅ Successfully extracted {len(df)} cookies from Brave on Windows!")
    print(f"   • Raw cookies saved to : {raw_file}")
    print(f"   • Columns: domain, name, value, path, expires_utc, secure, httpOnly,etc.")
