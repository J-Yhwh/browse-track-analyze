# Copyright (c) 2026. Jac LL.
# All Rights Reserved. 

# Cookie extraction for WindowsOS (mainly Chrome, Brave, Edge , Firefox, Opera,etc)
# Masterlist of extraction technique & csv

import os
import sqlite3
import shutil
import tempfile
import json
import base64
import pandas as pd


from pathlib import Path
from datetime import datetime, timedelta


try:
    import win32crypt          # pip install pywin32
except ImportError:
    win32crypt= None

from Crypto.Cipher import AES  # pip install pycryptodome


# ===================================================== PATH =======================================================

LOCAL = Path(os.environ["LOCALAPPDATA"])
ROAMING = Path(os.environ["APPDATA"])

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(exist_ok=True)


# ====================================================== HELPERS ====================================================

def add_metadata(df: pd.DataFrame, browser: str) -> pd.DataFrame:
    df = df.copy()
    df["browser"] = browser
    df["os"] = "Windows"
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df


def save_clean_cookies(df: pd.DataFrame, output_path: Path) -> None:
    columns = ["name", "value", "domain","path", "expires", "secure", "httpOnly"]
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df[columns].to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ Saved{len(df)} cookies  -> {output_path}")


def chrome_time_to_unix(chrome_time):
    """Convert Chrome's microseconds-since-1961 to unix timestamp."""
    if chrome_time == 0 or chrome_time is None:
        return None
    try:
        return(datetime, 1601, 1, 1) + timedelta(microseconds=chrome_time).timestamp()
    except Exception:
        return None


# ========================= CHROMIUM DECRYPTION (Chrome / Brave / Edge / Opera) =======================================

def get_chromium_key(local_state_path: Path) -> bytes:
    """Get the AES key from the Local State (DPAPI protected)."""
    if not local_state_path.exists():
        raise FileNotFoundError(f"Local state not found: {local_state_path}")


    with open(local_state_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    encrypted_key = base64.b64decode(data["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]   # remove DPAPI prefix "DPAPI"

    if win32crypt is None:
        raise ImportError("pywin32 is required for Windows Chromium decryption")

    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key



def decrypt_chromium_value(encrypted_value, aes_key):
    if not encrypted_value:
        return ""

    try:
        # v10 / v20 prefix
        if encrypted_value.startswith(b"v10") or encrypted_value.startswith(b"v20"):
            nonce = encrypted_value[3:15]
            ciphertext = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            return AESGCM(aes_key).decrypt(nonce, ciphertext + tag, None).decode(
                "utf-8", errors="replace"
            )
        return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode(
            "utf-8", errors="replace"
        )
    except Exception:
        return ""
          

def extract_chromium_browser(name: str, user_data_dir: Path, profile: str = "Default"):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting {name} cookie extraction...")

    cookie_db = user_data_dir / profile / "Network" / "Cookies"
    # Fallback for older versions
     
    if not cookie_db.exists():
        cookie_db = user_data_dir / profile / "Cookies"

    local_state_path = user_data_dir / "Local State"

    if not cookie_db.exists():
        print(f"❎ {name} cookies database not found.")
        return None


    try:
        key = get_chromium_key(local_state)

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_db = Path(tmpdir) / "Cookies"
            shutil.copy2(cookie_db, temp_db)

            # Copy WAL/SHM if present
            for suffix in ["-wal", "-shm"]:
                extra = Path(str(cookie_db) + suffix)
                if extra.exists():
                    shutil.copy2(extra, Path(temp_db) + suffix)

            conn = sqlite3.connect(temp_db)
            query = """
                SELECT host_key, name, encrypted_value, path, expires_utc,
                       is_secure, is_httponly
                FROM cookies
            """
            rows = conn.execute(query).fetchall()
            conn.close()

        cookies = []
        for host, name_, enc_val, path, expires, secure, httponly in rows:
            value = decrypt_chromium_value(enc_val, key)
            cookies.append({
                "domain": host,
                "name": name_,
                "value": value,
                "path": path,
                "expires": chrome_time_to_unix(expires),
                "secure": bool(secure),
                "httpOnly": bool(httponly),
            })

        df = pd.DataFrame(cookies)
        df = add_metadata(df, name)
        save_clean_cookies(df, DATA_FOLDER / f"{name.lower()}_Windows_cookies.csv")
        print(f"✅ Extracted {len(df)} {name} cookies")
        return df

    except Exception as e:
        print(f"{name} extraction  failed: {e}")
        return None




# ===============================================   FIREFOX ===========================================


def extract_firefox():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Firefox cookie extraction...")

    profiles_path = ROAMING /"Mozilla" / "Firefox" /  "Profiles"
    if not profiles_path.exists():
        print("❎ Firefox profile folders not detected.")
        return None

    #First test default-release, followed by any-default
    profile_dirs = list(profiles_path.glob("*.default-release")) + list(profiles_path.glob("*.default*"))
    if not profile_dirs:
        print(f"❎ No default Firefox profile found.")
        return None

    cookies_db = profile_dirs[0] / "cookies.sqlite"
    if not cookies_db.exists():
        print(f"No Firefox cookies.sqlite databses found")
        return None


    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_db = Path(tmpdir) /"cookies.sqlite"
            shutil.copy2(cookies_db, temp_db)

            conn = sqlite3.connect(temp_db)
            query = """
                SELECT host, name, value, path, expiry,
                       is_secure, isHttpOnly
                FROM moz_cookies
            """
            df = pd.read_sql_query(query, conn)
            conn.close()


        df = df.rename(columns={
            "host": "domain",
            "expiry": "expires",
            "is_secure": "secure",
            "isHttpOnly": "httpOnly"
        })


        df = add_metadata(df, "Firefox")
        save_clean_cookies(df, DATA_FOLDER / "firefox_Windows_cookies.csv")
        print(f"✅ Extracted {len(df)}Firefox cookies")
        return df

    except Exception as e:
        print(f"❎ Firefox extraction failed: {e}")
        return None



# ========================================== MAIN SCRAPING FOLDER PATH (BROWSERS) =========================================


if __name__ == "__main__":
    print("Windows cookie extraction...\n")


    # Brave
    extract_chromium_browser(
        "Brave",
        LOCAL / "Google" / "BraveSoftware" / "Brave-Browser" / "User Data"
    )


    # Chrome
    extract_chromium_browser(
        "Chrome",
        LOCAL / "Google" / "Chrome" / "User Data"
    )


    # Edge
    extract_chromium_browser(
        "Edge",
        LOCAL / "Microsoft" / "Edge" / "User Data"
    )


    # Opera
    extract_chromium_browser(
        "Opera",
        LOCAL / "Opera Software" / "Opera Stable"
    )


    # FIrefox
    extract_firefox()


    print("\n ✅ Windows extractions completed.")


    


    
        
        
