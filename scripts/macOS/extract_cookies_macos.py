# Copyright (c) 2026. Jac LL.
# All Rights Reserved. 

import os
import sqlite3 
import shutil
import tempfile
import subprocess
import pandas as pd
import browser_cookie3

from pathlib import Path
from datetime import datetime
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES



PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FOLDER = PROJECT_ROOT/ "data"
DATA_FOLDER.mkdir(exist_ok=True)




# ============================ HELPERS ===============================

def add_metadata(df:pd.DataFrame, browser: str) -> pd.DataFrame:
    """Only adds metadata columns."""
    df = df.copy()
    df["browser"] = browser
    df["os"] = "macOS"
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    return df


def save_clean_cookies(df:pd.DataFrame, output_path: Path) -> None:
    """Keeps only the original columns and saves the clean CSV."""
    columns_to_keep = ["name", "value", "domain","path", "expires", "secure", "httpOnly"]     # Sift out unnecessary details to keep the main/relevant columns 
    
    # Ensuring the existence of all required columns for consistency
    missing = [col for col in columns_to_keep if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df_clean = df[columns_to_keep].copy()


    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False, encoding="utf-8")
    
    print(f"✅ Saved {len(df)} cookies in the original clean format -> {output_path}")
    

# ============================= SAFARI ================================


def extract_safari():
    """
    Extracting cookies from MacOS using browser_cookie3
    """
    cookie_db = Path.home()/ "Library/Cookies/Cookies.binarycookies"   #Safari uses a binary format
    print(f"[{datetime.now().strftime('%H:%M:%S')}]  Starting Safari cookie extraction...")

    cookie_path = os.path.expanduser("~/Library/Containers/com.apple.Safari/Data/Library/Cookies/Cookies.binarycookies")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Safari cookie extraction...")


    try:
        cj = browser_cookie3.safari()
    
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

        if not cookies:
            print("⛔️ Safari cookie jar is empty.")
            return None

        df = pd.DataFrame(cookies)
        df = add_metadata(df, "Safari")
        save_clean_cookies(df, DATA_FOLDER / "safari_cookies_macos.csv")      #  Converted CSV file to save for analytics/ Streamlit

        print(f"✅ Extracted {len(df)} Safari cookies")
        return df

    
    except Exception as e:
        print(f"❌ Safari extracted failed: {e}")
        import traceback
        traceback.print_exc()
        return None



# ============================== BRAVE ================================


def extract_brave():
    print(f"[{datetime.now().strftime('&H:%M:%S')}] Starting Brave cookie extraction....")


    cookie_db = Path.home() / "Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies"

    if not cookie_db.exists():
        print("❌ Brave cookies not found.")
        None

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_db = Path(tmpdir) / "Cookies"
            shutil.copy2(cookie_db, temp_db)

            conn = sqlite3.connect(temp_db)
            query = """
                SELECT
                    host_key AS domain,
                    name,
                    value,
                    path,
                    expires_utc AS expires,
                    is_secure AS secure,
                    is_httponly AS httpOnly,
                    creation_utc,
                    last_access_utc
                FROM cookies
            """
            df = pd.read_sql_query(query, conn)
            conn.close()


        df = add_metadata(df, "Brave")
        save_clean_cookies(df, DATA_FOLDER / "brave_macos_cookies.csv")
        print(f"✅ Extracted {len(df)} Brave cookies")
        return df

    except Exception as e:
        print(f" Brave cookies extraction failed:  {e}")
        return None



# ============================= FIREFOX ==================================


def extract_firefox():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Firefox cookie extraction...")

    
    profiles_path = Path.home() /"Library/Application_support/Firefox/Profiles"
    profile_dirs = list(profiles_path.glob("*.default*"))

    if not profile_dirs:
        print("❌ No Firefox file found.")
        return None

    cookies_db = profile_dirs[0] / "cookies.sqlite"

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_db = Path(tmpdir) / "cookies.sqlite"
            shutil.copy2(cookies_db, temp_db)

            conn = sqlite3.connect(temp_db)
            query = """
                SELECT
                host_key AS domain,
                name,
                value,
                path,
                expiry AS expires,
                isSecure AS secure,
                isHttpOnly AS httpOnly,
                creationTime,
                lastAccessed
            FROM moz_cookies
            """
            df = pd.read_sql_query(query, conn)
            conn.close()


        df = add_metadata(df, "Firefox")
        save_clean_cookies(df, DATA_FOLDER / "firefox_macos_cookies.csv")
        print(f"✅ Extracted {len(df)} Firefox cookies.")
        return df

    except Exception as e:
        print(f" ⛔️Firefox extraction failed: {e}")
        return None


# ============================= CHROMIUM KEY + DECRYPT ======================


def get_chromium_key():
    """Retrieve Chrome / Opera safe storage key from MacOS keychain."""
    try:
        cmd = ['security','find-generic-password','-w','-a','Chrome','-s', 'Chrome Safe Storage']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        password = result.stdout.strip()
        if password:
            print(f"✅ Retrieved Chrome Safe Storage key ({len(password)} chars)")
            return password
    except subprocess.CalledProcessError:
        print(f"❌ Chrome key not found. Trying Opera Safe Storage...")
        try:
            cmd = ['security','find-generic-password','-w','-a','Opera','-s', 'Opera Safe Storage']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            password = result.stdout.strip()
            if password:
                print(f"✅ Retrieved Opera safe storage key as fallback.")
                return password
        except subprocess.CalledProcessError:
            pass
    raise Exception("Could not retrieve decryption key from Keychain.")



def decrypt_chromium_value(encrypted_value, key):
    """Decrypt Chromium-style encrypted cookie value"""
    if not encrypted_value or not isinstance(encrypted_value, bytes) or not encrypted_value.startswith(b'v10'):
        if isintance(encrypted_value, bytes):
            return encrypted_value.decode('utf-8', errors='ignore')
        return str(encrypted_value)


    try:
        nonce = encrypted_value[3:15]
        ciphertext = encrypted_value[15:-16]
        tag = encrypted_value[-16:]
        cipher = AES.key(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertecx.tag)
        return decrypted.decode('utf-8', errors='ignore')
    except Exception:
        return "[Decryption failed]"



# ============================== OPERA ======================================


def extract_opera():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Opera cookies extraction...")

    possible_paths = [
        Path.home() / "Library/Application Support/com.operasoftware.Opera/Default/Cookies",
        Path.home() / "Library/Application Support/com.operasoftware.Opera/Opera/Default/Cookies",
        Path.home() / "Library/Application Support/com.operasoftware.Opera/Profile 1/Cookies",
    ]

    cookies_db = next((p for p in possible_paths if p.exists()), None)
    if not cookies_db:
        print("❌ Opera cookies database not found.")
        return None

    print(f"✅ Found Opera cookies at: {cookies_db}")

    
    try:
        cmd = ['security','find-generic-password','-w','-a','Opera','-s','Opera Safe Storage']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        password = result.stdout.strip()
        if password:
            print(f"✅ Retrieved Opera Safe Storage key {len(password)} chars) ")
            return password
    except  subprocess.CalledProcessError:
        print("⛔️ Could not get Opera key. Trying Chrome Safe as fallback...")
        try:
            cmd = ['security','find-generic-password','-w','-a','Chrome','-s','Chrome Safe Storage']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            password = result.stdout.strip()
            if password:
                print(f"✅ Retrieved Chrome Safe Storage key as fallback ")
                return password
        except subprocess.CalledProcessError:
            pass
    raise Exception("Could not retrieve decryption key from Keychain. Unlock 'Opera Storage' in Keychain Access.")



def decrypt_opera_value(encrypted_value, key):
    """Decrypt Chromium-style encrypted cookie value"""
    if not encrypted_value or not encrypted_value.startswith(b'v10'):
        return encrypted_value.decode('utf-8', errors='ignore')
    return str(encrypted_value)



    try:
        nonce = encrypted_value[3:15]
        ciphertext = encrypted_value[15:-16]
        tag = encrypted_value[-16]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode('utf-8', errors='ignore')
    except Exception:
        return "[Decryption failed]"



def extract_opera():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Opera cookie extraction...")

    possible_paths = [
        Path.home() / "Library/Application Support/com.operasoftware.Opera/Default/Cookies",
        Path.home() / "Library/Application Support/com.operasoftware.Opera/Opera/Default/Cookies",
        Path.home() / "Library/Application Support/com.operasoftware.Opera/Profile 1/Cookies",
    ]

    cookies_db = next((p for p in possible_paths if p.exists()), None)
    if not cookies_db:
        print(" ❌ Opera Cookies database not found.")
        return None


    print(f"✅ Found Opera cookies at: {cookies_db}")

    try:
        key = get_chromium_key()
        # Use the actual AES key (Opera/Chrome uses PBKDF2)
        aes_key = PBKDF2(key, b'saltysalt', dkLen=16, count=1003)

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_db = Path(tmpdir) / "Cookies"
            shutil.copy2(cookies_db, temp_db)

            conn = sqlite3.connect(temp_db)
            query = """
                SELECT host_key, name, encrypted_value, path, expires_utc,
                    is_secure, is_httponly, creation_utc
                FROM cookies
            """
            rows = conn.execute(query).fetchall()
            conn.close()


        if not rows:
            print(" ⛔️ No cookiea found in Opera database.")
            return None


        cookies = []
        for row in rows:
            domain, name, enc_val, path, expires_utc, secure, httponly, created = row
            value = decrypt_chromium_value(enc_val, aes_key)
            cookies.append({
                "domain": domain,
                "name": name,
                "value": value,
                "path" : path,
                "expires": expires_utc,
                "secure": bool(secure),
                "httpOnly": bool(httponly),
                "creation_utc": created,
            })

        df = pd.DataFrame(cookies)
        df = add_metadata(df, "Opera")
        save_clean_cookies(df, DATA_FOLDER / "opera_macos_cookies.csv")
        print(f" ✅ Extracted {len(df)} Opera cookies.")
        return df

    except Exception as e:
        print(f"⛔️ Opera extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return None



# =================================== CHROME ====================================

def extract_chrome():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Chrome Cookie extraction...")

    possible_paths = [
        Path.home() / "Library/Application Support/Google/Chrome/Default/Cookies",
        Path.home() / "Library/Application Support/Google/Chrome/Profile 1/Cookies",
    ]

    cookie_db = next((p for p in possible_paths if p.exists()), None)
    if not cookie_db:
        print("❌ Chrome cookies database not found.")
        return None


    print(f"✅ Found Chrome cookies at: {cookie_db}")


    try:
        # resuse the same decrypted AES keys (from Crypto.Cipher library) for Opera 
        key = get_chromium_key()
        aes_key = PBKDF2(key, b'saltysalt', dkLen=16, count=1003)
    
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_db = Path(tmpdir) / "Cookies"
            shutil.copy2(cookie_db, temp_db)

            conn = sqlite3.connect(temp_db)
            query = """
                SELECT
                    host_key, name, encrypted_value, path, expires,
                    is_secure, is_httponly, creation_utc,
                FROM cookies
            """
            rows = conn.execute(query).fetchall()
            conn.close()

        if not rows:
            print(" ⛔️ No cookies found in Chrome database.")
            return None
            

        cookies = []
        for row in rows:
            domain, name, enc_value, path, expires_utc, secure, httponly, crested = row
            value = decrypt_chrome_value(enc_val, aes_key)
            cookies.append({
                "domain": domain,
                "name": name,
                "value": value,
                "path": path,
                "expires_utc": expires,
                "secure": bool(secure),
                "httpOnly": bool(httponly),
                "creation_utc": created,
            })


        df = pd.DataFrame(cookies)
        df = add_metadata(df, "Chrome")
        save_clean_cookies(df, Path("chromes_macos_cookies.csv"))
        print(f"Extracted {len(df)} Chrome cookies.")
        return df

    except Exception as e:
        print(f"Chrome extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return None




# ============================== MAIN =====================================

if __name__ == "__main__":
    print("🍎 MacOS cookie extraction ...\n")

    extract_safari()
    extract_brave()
    extract_firefox()
    extract_opera()
    extract_chrome()


    print("\n✅ MacOS extractions completed.")


    
            
    


        
    


    
