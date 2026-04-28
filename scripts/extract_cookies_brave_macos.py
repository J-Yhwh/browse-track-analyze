import sqlite3
import csv
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


# ===================================================
# CONFIGURATION
# ===================================================
REPO_ROOT = Path.home() / "Desktop" / "main"
DATA_FOLDER = REPO_ROOT / "data"
DATA_FOLDER.mkdir(exist_ok=True, parents=True)

COOKIES_PATH = Path.home() / "Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies"
BACKUP_PATH = DATA_FOLDER / "cookies_backup.db"
OUTPUT_CSV = DATA_FOLDER / "brave_macos_cookies.csv"

def get_decryption_key():
    try:
        # Try Brave first
        cmd = ['security', 'find-generic-password', '-w', '-a', 'Brave', '-s', 'Brave Safe Storage']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        password = result.stdout.strip()
        print(f"Retrieved Brave Safe Storage password (length: {len(password)} chars)")
        if password:
            return password
    except subprocess.CalledProcessError:
        print("Brave Safe Storage entry not found or access denied.")

    # Fallback to Chrome Safe Storage (common in Brave)
    try:
        cmd = ['security', 'find-generic-password', '-w', '-a', 'Chrome', '-s', 'Chrome Safe Storage']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        password = result.stdout.strip()
        print(f"Retrieved Chrome Safe Storage password (length: {len(password)} chars)")
        if password:
            return password
    except subprocess.CalledProcessError:
        raise Exception(
            "Could not retrieve any Safe Storage key.\n"
            "1. Open Keychain Access → search 'Safe Storage'\n"
            "2. Look for 'Brave Safe Storage' or 'Chrome Safe Storage'\n"
            "3. Double-click → Access Control → 'Allow all applications' or add 'Terminal'/'python'\n"
            "4. Save Changes (enter macOS password)\n"
            "5. Log into a site in Brave to force cookie creation, then retry."
        )

def decrypt_value(encrypted_value, key):
    """
    Decrypts Brave/Chrome cookie value using AES-GCM (v10 format).
    Forces bytes safety to avoid C-code type errors.
    """
    if not encrypted_value:
        return ""

    # Force encrypted_value to bytes (SQLite can sometimes return str-like)
    if isinstance(encrypted_value, str):
        encrypted_value = encrypted_value.encode('latin1')  # preserves raw bytes

    if not encrypted_value.startswith(b'v10'):
        return encrypted_value.decode('utf-8', errors='ignore')

    try:
        # Force slices to bytes (extra safety)
        nonce = bytes(encrypted_value[3:15])          # 12-byte nonce
        ciphertext = bytes(encrypted_value[15:-16])   # ciphertext
        tag = bytes(encrypted_value[-16:])            # 16-byte tag

        # Debug prints (remove after testing)
        print(f"Nonce type: {type(nonce)}, length: {len(nonce)}")
        print(f"Ciphertext type: {type(ciphertext)}, length: {len(ciphertext)}")
        print(f"Tag type: {type(tag)}, length: {len(tag)}")
        print(f"Key type: {type(key)}, length: {len(key)}")

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode('utf-8', errors='ignore')
    except ValueError as e:
        return f"[MAC check failed: {str(e)} - likely wrong key or format]"
    except TypeError as e:
        return f"[Type Error: {str(e)} - forced bytes conversion needed]"
    except Exception as e:
        return f"[Decryption Error: {str(e)}]"


    
def extract_brave_cookies():
    if not COOKIES_PATH.exists():
        print(f"Error: Cookies DB not found at {COOKIES_PATH}")
        return

    print("Backing up Cookies database...")
    shutil.copy(COOKIES_PATH, BACKUP_PATH)

    conn = None
    cursor = None
    key = None

    try:
        key = get_decryption_key()
        conn = sqlite3.connect(BACKUP_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                host_key AS domain,
                name,
                encrypted_value,
                path,
                expires_utc,
                is_secure,
                is_httponly,
                creation_utc
            FROM cookies
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No cookies found in database. Visit some sites in Brave and try again.")
            return

        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'domain', 'name','path', 'expires_utc',
                'is_secure', 'is_httponly', 'creation_utc',
                'expires_date', 'creation_date'
            ])

            for row in rows:
                domain, name, enc_val, path, expires_utc, secure, httponly, creation_utc = row

                expires_date = "Never"
                if expires_utc and expires_utc > 0:
                    try:
                        expires_unix = (expires_utc // 1000000) - 11644473600
                        expires_date = datetime.fromtimestamp(expires_unix).strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        expires_date = "Invalid"

                creation_date = "Unknown"
                if creation_utc:
                    try:
                        creation_unix = (creation_utc // 1000000) - 11644473600
                        creation_date = datetime.fromtimestamp(creation_unix).strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        creation_date = "Invalid"

                writer.writerow([
                    domain, name, path, expires_utc,
                    bool(secure), bool(httponly), creation_utc,
                    expires_date, creation_date
                ])

        print(f"Success! Exported {len(rows)} decrypted cookies to {OUTPUT_CSV}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        if BACKUP_PATH.exists():
            BACKUP_PATH.unlink()
            print("Temporary backup deleted.")

if __name__ == "__main__":
    extract_brave_cookies()
