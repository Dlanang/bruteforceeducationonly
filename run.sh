#!/bin/bash

# Banner
echo "=================================="
echo "        Running MR.FOX v0.8       "
echo "=================================="

# Cek apakah wordlist.txt ada
if [ ! -f "wordlist.txt" ]; then
    echo "[ERROR] wordlist.txt tidak ditemukan di direktori ini."
    exit 1
fi

# Install dependencies jika belum
echo "[INFO] Mengecek dan meng-install dependensi..."
pip install -r requirements.txt

# Jalankan script Python
echo "[INFO] Menjalankan bruteforce.py..."
python3 bruteforce.py
