# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.

import hashlib
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

# Possible Edge profile paths
# NOTE: Please replace all "FILEPATH" portion of the directory paths with the account/profile name of your local folder(s)
base_path = Path(r"C:\FILEPATH\AppData\Local\Microsoft\Edge\User Data")

possible_profiles = ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4"]

found = False

for profile in possible_profiles:
    cookie_db_path = base_path / profile / "Network" / "Cookies"
    
    print(f"Checking: {cookie_db_path}")
    
    if cookie_db_path.exists():
        print(f"   ✅ Found Cookies database! Size: {cookie_db_path.stat().st_size / 1024:.1f} KB")
        
        try:
            conn = sqlite3.connect(cookie_db_path)
            conn.row_factory = sqlite3.Row
            
            count = conn.execute("SELECT COUNT(*) FROM cookies").fetchone()[0]
            print(f"   ✅ Number of cookies: {count:,}")
            
            # Extract data
            query = """
            SELECT 
                host_key AS domain,
                name,
                value,
                path,
                expires_utc,
                is_secure AS secure,
                is_httponly AS httpOnly,
                creation_utc AS creation_time
            FROM cookies
            ORDER BY host_key, name
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()

            # This safely converts every single row value in the pandas column into a SHA-256 string
            df['value'] = df['value'].apply(lambda x: hashlib.sha256(str(x).encode('utf-8')).hexdigest() if pd.notna(x) and x != "" else "")
            
            # Save
            desktop = Path(r"C:\FILEPATH\OneDrive\Desktop")
            raw_file = desktop / "edge_cookies_raw.csv"
            
            df['browser'] = "Edge"
            df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            df.to_csv(raw_file, index=False, encoding="utf-8")
            
            print(f"   ✅ Saved {len(df)} cookies to: {raw_file}")
            found = True
            break
            
        except Exception as e:
            print(f"   ❌ Error reading database: {e}")
    else:
        print("   ❌ Not found")

if not found:
    print("\n❌ Could not find Edge Cookies database in common locations.")
    print("Please check your Edge profile folder manually.")
