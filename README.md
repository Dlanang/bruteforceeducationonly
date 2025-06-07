Berikut adalah dokumentasi dalam format **Markdown** (`README.md`) untuk proyek `MR.FOX` v0.8:

---

````markdown
# 🦊 MR.FOX v0.8

**MR.FOX** adalah tools ethical hacking yang berfokus pada _brute force_ login form berbasis web, cocok untuk skenario **pentest jaringan internal**. Tools ini berjalan murni menggunakan **Python**, dilengkapi fitur:

- Deteksi otomatis form login
- Auto-fix URL tanpa skema (`http://`)
- Multi-threaded brute force
- ASCII banner ala hacker
- Laporan hasil brute force
- Validasi & error handling
- Simple wordlist integration (`wordlist.txt`)

---

## 🚀 Cara Instalasi

```bash
# 1. Clone repositori (jika sudah diupload)
git clone https://github.com/yourname/mrfox.git
cd mrfox

# 2. Buat environment virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instal dependency
pip install -r requirements.txt

# 4. Jalankan program
./run.sh
````

## 📄 Struktur Proyek

 
MR.FOX/
├── bruteforce.py        # File utama
├── ascii.py             # ASCII banner
├── wordlist.txt         # Wordlist kombinasi username:password
├── run.sh               # Script eksekusi
├── requirements.txt     # Dependency Python
└── .gitignore
```

---

## ⚙️ Penggunaan

Setelah menjalankan `./run.sh`, Anda akan melihat banner:

```text

 _      ____      _____ ____ ___  _
/ \__/|/  __\    /    //  _ \\  \//
| |\/|||  \/|    |  __\| / \| \  / 
| |  |||    /__  | |   | \_/| /  \ 
\_/  \|\_/\_\\/  \_/   \____//__/\\
                                   
 v0.8
```

### Input

```
Masukkan target URL (contoh: 192.168.1.1/login):
```

> Anda bisa input tanpa `http://` → akan otomatis diperbaiki.

## 📊 Output

Hasil percobaan brute-force akan ditampilkan di terminal dan disimpan dalam:

```
report.txt
```

Contoh isi:

```
Berhasil -> admin:admin123 | Respon Length: 1745
```

## 💡 Catatan

* Gunakan `wordlist.txt` dalam folder root proyek.
* Tools ini *tidak menggunakan* tools eksternal seperti `ffuf` untuk menjaga portabilitas.
* Cocok untuk pentest internal dan latihan edukasi.

## ✅ Fitur Mendatang (roadmap)

* [ ] Deteksi method `GET/POST`
* [ ] Simulasi User-Agent acak
* [ ] Export laporan dalam format `.json` dan `.csv`
* [ ] GUI mode
* [ ] Integrasi bypass rate-limit dasar

## ⚠️ Legal

> Tools ini hanya untuk **keperluan edukasi dan pentesting legal**. Segala penyalahgunaan di luar izin target bukan tanggung jawab developer.

## 🧠 Author

**MR.FOX** by [Lanang](mailto:ceo@dhimaslanangnugroho.my.id) 🦊
Red Team Project • 2025
