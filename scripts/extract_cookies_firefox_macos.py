import sqlite3
import shutil
import pandas as pd

from pathlib import Path
from datetime import datetime
import tempfile


# Path to cookies
def get_firefox_cookies_macos():
    profiles_path = Path.home() / "Library/Application Support/Firefox/Profiles"

    if not profiles_path.exists():
        print("❌ Firefox Profiles folder not found.")
        return

    # Find default profile (usually ends with 'default-release')
    profile_dirs = list(profiles_path.glob("*.default*"))
    if not profile_dirs:
        print("❌ No Firefox profile found.")
        return

    profile_dir = profile_dirs[0]  #take the forst matching profile
    cookies_db = profile_dir / "cookies.sqlite"

    if not cookies_db.exists():
        print(f"cookies.sqlite not found in {profile_dir.name}")
        return

    print(f"✅ Found Firefox profile: {profile_dir.name}")

    # Copy the database becaue Firefox locks the original
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_db = Path(tmpdir) /"cookies.sqlite"
        shutil.copy2(cookies_db, temp_db)

        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row


        query = """
        SELECT
            host AS domain,
            name,
            value,
            path,
            expiry AS expires,
            isSecure AS secure,
            isHttpOnly as httpOnly,
            creationTime as creation_time,
            lastAccessed as last_access_time
        FROM moz_cookies
        ORDER by host, name
        """

        df = pd.read_sql_query(query, conn)
        conn.close()

    #Add metadata
    df["browser"] = "firefox"
    df["os"] = "macOS"
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to csv file data folder
    output_path = Path("data") / "firefox_macos_cookies.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Extracted {len(df)} cookies")
    print(f" Saved to: {output_path}")


if __name__ == "__main__":
    get_firefox_cookies_macos()
        






