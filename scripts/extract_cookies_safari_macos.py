import browser_cookie3
import traceback
import pandas as pd

import os
from datetime import datetime
import time


# === IMPORTANT: EXPLICIT PATH TO DATA FOLDER FROM PROJECT ROOT DIRECTORY===
project_root = os.path.expanduser("~/Desktop/Track-analyze-main")
data_folder = os.path.join(project_root, "data")
os.makedirs(data_folder, exist_ok=True)

print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Safari cookie extraction...")
print(f"📁 Saving to folder: {data_folder}")

cookie_path = os.path.expanduser("~/Library/Containers/com.apple.Safari/Data/Library/Cookies/Cookies.binarycookies")
print(f"Looking for Safari cookie file at: {cookie_path}")

if not os.path.exists(cookie_path):
    print("❌ Cookie file not found!")
    print("   → Open Safari, browse some sites, log into accounts, then quit Safari completely.")
    exit()

print("✅ Cookie file found. Parsing...")

time.sleep(2)


try:
    print("Step 1: Calling browsercookie.safari()...")
    cj = browser_cookie3.safari()
    print(f"Step 2: Cookie jar returned — iterating...")
    
    cookies = []
    for cookie in cj:
        cookies.append({
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
            'expires': cookie.expires,
            'secure': cookie.secure,
            'httpOnly': cookie.has_nonstandard_attr('HttpOnly'),
        })
    
    print(f"Step 3: Loop complete. Cookies collected: {len(cookies)}")

    if cookies:
        df = pd.DataFrame(cookies)
        output_path = os.path.join(data_folder, "safari_cookies_full.csv")
        print(f"Step 4: Writing CSV to {output_path}...")
        df.to_csv(output_path, index=False)
        print(f"✅ Done! File exists: {os.path.exists(output_path)}")
        print(df.head())
    else:
        print("⚠️ Cookie jar was empty — nothing to save.")

except Exception as e:
    import traceback
    print(f"❌ Error at step: {e}")
    traceback.print_exc()


    
