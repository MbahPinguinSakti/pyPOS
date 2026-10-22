# 🛒 pyPOS - Point of Sale System

**pyPOS** adalah sistem kasir (Point of Sale) berbasis web yang dibangun menggunakan **Django**, didukung dengan antarmuka modern menggunakan **Tailwind CSS** dan **DaisyUI**.

---

## 🌟 Fitur Utama

- **📦 Manajemen Stok & Konversi Fleksibel**:
  - Mendukung stok ganda: **Eceran (satuan)** dan **Lusinan (box)**.
  - Rasio konversi fleksibel per produk (misal: 1 box = 12 pcs).
  - Otomatis melakukan *box unpacking* (membongkar stok lusinan) saat stok eceran tidak mencukupi selama transaksi.
- **💳 Kasir & Checkout Interaktif**:
  - Pemilihan produk langsung dengan kalkulasi subtotal instan via JavaScript.
  - Pilihan tipe jual: *Eceran* atau *Lusinan*.
  - Perhitungan kembalian otomatis dan tombol jalan pintas "Uang Pas".
- **🧾 Struk Transaksi & Riwayat**:
  - Detail transaksi lengkap dengan rincian harga beli, harga jual, dan waktu.
  - Tombol **Cetak Struk** (*Print*) dan **Unduh Struk Teks** (*Download .txt*).
  - Riwayat seluruh transaksi dengan estimasi pendapatan dan laba (*profit*).
- **🎨 Tampilan Modern & Responsif**:
  - Dark mode bawaan (*Dracula theme*).
  - Sidebar navigasi responsif dengan Drawer (*mobile friendly*).

---

## 📁 Struktur Direktori

```text
pyPOS/
├── docs/                      # Dokumentasi & spesifikasi
│   └── prompt.md
├── real/                      # Konfigurasi proyek Django (Settings & Root URL)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── static/                    # Aset statis (CSS, JS, gambar)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── store/                     # Aplikasi utama Point of Sale
│   ├── __init__.py
│   ├── admin.py               # Konfigurasi Django Admin
│   ├── apps.py
│   ├── migrations/            # Migrasi database
│   ├── models.py              # Model Product, Transaction, TransactionItem
│   ├── tests.py               # Unit tests (Model & View)
│   ├── urls.py                # Routing aplikasi store
│   └── views.py               # Logika transaksi, dashboard, restock
├── templates/                 # Template HTML (Django Templates)
│   ├── base.html              # Layout induk (Drawer, Navbar, CDN)
│   ├── components/            # Komponen UI reusable (card, button, input, radio)
│   ├── snippets/              # Snippet layout (navbar, cdn)
│   └── store/                 # Halaman aplikasi (index, make, detail, history, restock)
├── .env.example               # Contoh konfigurasi variabel lingkungan
├── .gitignore                 # File yang diabaikan oleh Git
├── manage.py                  # CLI Django
├── README.md                  # Dokumentasi proyek
└── requirements.txt           # Dependensi Python
```

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Kloning Repositori
```bash
git clone https://github.com/MbahPinguinSakti/pyPOS.git
cd pyPOS
```

### 2. Buat & Aktifkan Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux / macOS
# atau: .venv\Scripts\activate  # Windows
```

### 3. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Lingkungan (Opsional)
Salin file `.env.example` ke `.env`:
```bash
cp .env.example .env
```
Secara bawaan, aplikasi mendukung database `sqlite` (mudah digunakan langsung) dan `mysql`.

### 5. Jalankan Migrasi Database
```bash
python manage.py migrate
```

### 6. Jalankan Server Pengembangan
```bash
python manage.py runserver
```

Buka browser dan akses: `http://127.0.0.1:8000/`

---

## 🧪 Menjalankan Unit Tests

Untuk menjalankan rangkaian pengujian otomatis:
```bash
DB_ENGINE=sqlite python manage.py test
```

---

## 📜 Lisensi
Dikembangkan untuk kebutuhan manajemen kasir & inventori toko yang cepat, efisien, dan andal.
