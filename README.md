# 🛒 pyPOS

Aplikasi kasir (Point of Sale) berbasis web untuk toko kecil, dibangun dengan **Django** dan antarmuka **Tailwind CSS + DaisyUI**. Mendukung penjualan **eceran** maupun **lusinan/box**, dengan bongkar box otomatis saat stok eceran habis.

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)
![DaisyUI](https://img.shields.io/badge/DaisyUI-5-5A0EF8?logo=daisyui&logoColor=white)

---

## ✨ Fitur

**Stok eceran & lusinan**
- Setiap produk punya dua stok: eceran (satuan) dan lusinan (box).
- Rasio konversi diatur per produk (misalnya 1 box = 12 pcs).
- Kalau stok eceran kurang saat transaksi, sistem membongkar box secukupnya lalu menyimpan sisanya sebagai stok eceran.

**Kasir**
- Pilih produk, jumlah, dan tipe jual (eceran atau lusinan).
- Harga lusinan otomatis = harga eceran × isi box.
- Subtotal dan kembalian dihitung langsung di browser.
- Tombol **Uang Pas** untuk mengisi nominal bayar sesuai total.
- Transaksi disimpan secara atomik: kalau stok tidak cukup, tidak ada data yang tersimpan setengah jalan.

**Struk & riwayat**
- Halaman struk berisi rincian item, harga, total, bayar, dan kembalian.
- Struk bisa dicetak atau diunduh sebagai file `.txt`.
- Halaman riwayat menampilkan semua transaksi beserta total penjualan dan laba. Laba dihitung dari harga beli yang dicatat saat barang terjual, jadi tidak berubah walaupun harga produk diubah belakangan.

**Tampilan**
- Tema gelap *Dracula* dari DaisyUI.
- Sidebar berbentuk drawer, nyaman dipakai di layar HP.

---

## 🧰 Teknologi

| Bagian   | Yang dipakai                                                   |
| -------- | -------------------------------------------------------------- |
| Backend  | Python, Django 5.2                                             |
| Database | SQLite (pengembangan) atau MySQL                               |
| Frontend | Django Templates, Tailwind CSS 4, DaisyUI 5, Font Awesome (CDN) |

---

## 🚀 Instalasi

### 1. Clone repositori

```bash
git clone https://github.com/MbahPinguinSakti/pyPOS.git
cd pyPOS
```

### 2. Buat virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate         # bash / zsh
# source .venv/bin/activate.fish  # fish
# .venv\Scripts\activate          # Windows
```

### 3. Pasang dependensi

```bash
pip install -r requirements.txt
```

> `mysqlclient` butuh library MySQL/MariaDB di sistem (misalnya `libmysqlclient-dev` atau `mariadb-libs`). Kalau hanya memakai SQLite dan instalasinya gagal, paket ini boleh dilewati.

### 4. Atur environment variable

Konfigurasi dibaca dari environment variable. File `.env` **tidak** dimuat otomatis, jadi variabelnya perlu di-export dulu.

Penting: kalau `DB_ENGINE` tidak diisi, aplikasi memakai **MySQL**. Untuk mencoba cepat, pakai SQLite:

```bash
export DB_ENGINE=sqlite           # bash / zsh
# set -x DB_ENGINE sqlite         # fish
```

Daftar variabel lengkap ada di `.env.example`:

| Variabel               | Default     | Keterangan                                     |
| ---------------------- | ----------- | ---------------------------------------------- |
| `DB_ENGINE`            | `mysql`     | `sqlite` atau `mysql`                          |
| `DB_NAME`              | `test`      | Nama database MySQL                            |
| `DB_USER`              | `testuser`  | User MySQL                                     |
| `DB_PASSWORD`          | `123`       | Password MySQL                                 |
| `DB_HOST`              | `localhost` | Host MySQL                                     |
| `DB_PORT`              | `3306`      | Port MySQL                                     |
| `DJANGO_SECRET_KEY`    | (insecure)  | **Wajib diganti** untuk produksi               |
| `DJANGO_DEBUG`         | `True`      | Isi `False` untuk produksi                     |
| `DJANGO_ALLOWED_HOSTS` | `*`         | Daftar host dipisah koma                       |

### 5. Migrasi database & buat akun admin

```bash
python manage.py migrate
python manage.py createsuperuser   # opsional, untuk /admin/
```

### 6. Jalankan server

```bash
python manage.py runserver
```

Buka `http://127.0.0.1:8000/`.

---

## 🗺️ Halaman

| URL                    | Halaman                         |
| ---------------------- | ------------------------------- |
| `/`                    | Dialihkan ke dashboard          |
| `/store/`              | Dashboard: produk & transaksi terbaru |
| `/store/tambah/`       | Tambah produk / restock         |
| `/store/jual/`         | Kasir (buat transaksi)          |
| `/store/transaksi/<id>/` | Struk transaksi               |
| `/store/history/`      | Riwayat transaksi & laba        |
| `/admin/`              | Django Admin                    |

---

## 🧪 Testing

```bash
DB_ENGINE=sqlite python manage.py test     # bash / zsh
# env DB_ENGINE=sqlite python manage.py test  # fish
```

Tes mencakup model (`Product`, `Transaction`, `TransactionItem`) dan view, termasuk skenario jual eceran, bongkar box, jual lusinan, dan perhitungan laba.

---

## 📁 Struktur proyek

```text
pyPOS/
├── real/              # Konfigurasi proyek Django (settings, root URL, WSGI/ASGI)
├── store/             # Aplikasi kasir: model, view, URL, admin, tes
│   └── migrations/
├── templates/
│   ├── base.html      # Layout utama (drawer, navbar)
│   ├── components/    # Komponen UI: button, card, input, radio
│   ├── snippets/      # Navbar & tautan CDN
│   └── store/         # Halaman: index, make, detail, history, restock
├── static/            # CSS & JS
├── docs/              # Catatan desain
├── .env.example       # Contoh environment variable
├── manage.py
└── requirements.txt
```

---

## 🤝 Kontribusi

Issue dan pull request dipersilakan. Sebelum mengirim PR, pastikan `python manage.py test` lolos.

## 📜 Lisensi

Proyek ini belum memiliki lisensi. Tanpa lisensi, hak cipta tetap pada pemilik repositori.
