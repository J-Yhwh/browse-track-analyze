# Copyright (c) 2026. Jac LL
# All Rights Reserved. 
# Unauthorized use or distribution is prohibited.


import sqlite3
import csv
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import time

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

# ===================================================
# CONFIGURATION
# ===================================================
REPO_ROOT = Path.home() / "Desktop" / "Track-analyze-main"
DATA_FOLDER = REPO_ROOT / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)

OUTPUT_CSV = DATA_FOLDER / "opera_macos_cookies.csv"


def get_decryption_key():
    # 1. ALWAYS put the try block first to execute the command
    try:
        cmd = ['security', 'find-generic-password', '-w', '-a', 'Opera', '-s', 'Opera Safe Storage']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        password = result.stdout.strip()
        
        # 2. Check if we actually got a string back
        if password:
            print(f"✅ Retrieved Opera Safe Storage password ({len(password)} chars)")
            return password
        else:
            print("⚠️ Command ran but password string was empty.")
            
    # 3. Handle errors if the Opera key doesn't exist in Keychain
    except subprocess.CalledProcessError:
        print("⚠️ Could not retrieve Opera Safe Storage key. Trying Chrome fallback...")
        
        # 4. Fallback logic (Example: checking Chrome's keychain entry instead)
        try:
            cmd_chrome = ['security', 'find-generic-password', '-w', '-a', 'Chrome', '-s', 'Chrome Safe Storage']
            result_chrome = subprocess.run(cmd_chrome, capture_output=True, text=True, check=True)
            password_chrome = result_chrome.stdout.strip()
            if password_chrome:
                print(f"✅ Retrieved Chrome Safe Storage password ({len(password_chrome)} chars)")
                return password_chrome
        except subprocess.CalledProcessError:
            # If both fail, raise the final exception
            raise Exception("Could not get decryption key. Please unlock 'Opera Safe Storage' in Keychain Access.")


def decrypt_value(encrypted_value, key):
    if not encrypted_value or not encrypted_value.startswith(b'v10'):
        return encrypted_value.decode('utf-8', errors='ignore') if isinstance(encrypted_value, bytes) else str(encrypted_value)
    try:
        nonce = encrypted_value[3:15]
        ciphertext = encrypted_value[15:-16]
        tag = encrypted_value[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode('utf-8', errors='ignore')
    except:
        return "[Decryption failed]"

def extract_opera_cookies():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Opera cookie extraction...")

    # Try multiple possible profile paths
    possible_paths = [
        Path.home() / "Library/Application Support/OperaSoftware/Opera-Browser/Default/Cookies",
        Path.home() / "Library/Application Support/OperaSoftware/Opera-Browser/Profile 1/Cookies",
        Path.home() / "Library/Application Support/OperaSoftware/Opera-Browser/Profile 2/Cookies",
    ]

    cookies_db = None
    for path in possible_paths:
        if path.exists():
            cookies_db = path
            print(f"✅ Found cookies database at: {path}")
            break

    if not cookies_db:
        print("❌ Cookies database not found. Make sure Opera has been used.")
        return

    # Backup
    backup_path = DATA_FOLDER / "cookies_backup.db"
    shutil.copy(cookies_db, backup_path)
    print("📦 Backed up Cookies database")

    key = get_decryption_key()
    if not key:
        return

    conn = sqlite3.connect(backup_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cookies")
    count = cursor.fetchone()[0]
    print(f"Total rows in cookies table: {count}")

    cursor.execute("""
        SELECT host_key, name, encrypted_value, path, expires_utc, is_secure, is_httpOnly, creation_utc 
        FROM cookies
    """)
    rows = cursor.fetchall()

    if not rows:
        print("❌ No cookies found in database.")
        print("   → Make sure you have visited sites and logged into accounts in Brave.")
        print("   → Completely quit Opera (Cmd+Q) before running this script.")
    else:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['domain', 'name', 'value', 'path', 'expires_utc', 'secure', 'httpOnly', 'creation_utc'])
            for row in rows:
                domain, name, enc_val, path, expires_utc, secure, httpOnly, creation_utc = row
                value = decrypt_value(enc_val, key)
                writer.writerow([domain, name, value, path, expires_utc, secure, httpOnly, creation_utc])

        print(f"✅ SUCCESS! Exported {len(rows)} cookies to {OUTPUT_CSV}")

    # Cleanup
    cursor.close()
    conn.close()
    if backup_path.exists():
        backup_path.unlink()
        print("🗑️ Temporary backup deleted.")

if __name__ == "__main__":
    extract_opera_cookies()

    
