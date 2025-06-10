Bot Analisis Trading Kripto dengan AI
Bot Telegram canggih yang menyediakan analisis teknikal pasar kripto secara real-time. Dilengkapi dengan visualisasi candlestick chart dan analisis mendalam menggunakan Google Gemini AI, bot ini dirancang untuk membantu trader mengambil keputusan yang lebih baik.

Fitur Utama
🤖 Alur Percakapan Interaktif: Pengguna dipandu melalui menu yang jelas, mulai dari pemilihan token hingga analisis akhir.
📈 Visualisasi Chart: Secara otomatis menghasilkan dan mengirim gambar candlestick chart untuk token dan timeframe yang dipilih.
🧠 Analisis Berbasis AI: Menggunakan model Google Gemini untuk memberikan analisis teknikal, prediksi sentimen pasar, serta rekomendasi sinyal trading (Entry, Take Profit, Stop Loss) berdasarkan data OHLC terbaru.
🌐 Data Pasar Real-time: Terintegrasi langsung dengan API CoinGecko untuk mendapatkan data harga Open, High, Low, Close (OHLC) yang akurat.
⏳ Cooldown System: Mencegah spamming permintaan analisis dengan memberlakukan jeda waktu antar permintaan untuk setiap pengguna.
💾 Database Lokal: Menggunakan SQLite untuk menyimpan informasi pengguna, seperti waktu analisis terakhir untuk fitur cooldown.
Tampilan Bot
Pengguna memulai percakapan dan memilih token. 2. Bot menampilkan chart candlestick dan hasil analisis AI. ## Teknologi yang Digunakan
<!-- end list -->

Bahasa: Python 3
Framework Bot: python-telegram-bot
Model AI: Google Gemini
Sumber Data: CoinGecko API
Pembuatan Chart: matplotlib, mplfinance, pandas
Database: SQLite
Cara Menggunakan
Prasyarat
Python 3.8 atau yang lebih baru
Akun Telegram dan Token Bot
Kunci API untuk Google Gemini
Git
Instalasi
Clone repository ini:

Bash

git clone [URL-REPOSITORY-ANDA]
cd [NAMA-FOLDER-REPOSITORY]
Buat dan aktifkan virtual environment (dianjurkan):

Bash

python -m venv venv
source venv/bin/activate  # Di Windows, gunakan: venv\Scripts\activate
Install semua dependensi yang dibutuhkan:

Bash

pip install -r requirements.txt
Konfigurasi Kunci API:

Buka file config.py.
Masukkan TELEGRAM_TOKEN dan GEMINI_API_KEY Anda.
<!-- end list -->

Python

# config.py
TELEGRAM_TOKEN = "7207657126:AAF53TTiNB_VIQcl_8bk5DfYKgZ6laX8izU"  # Ganti dengan token Anda
GEMINI_API_KEY = "AIzaSyDsc31OGVg2Jwhhcwruqum6k2cef_prByo" # Ganti dengan kunci Gemini Anda
# ...
Menjalankan Bot
Setelah semua konfigurasi selesai, jalankan bot dengan perintah:

python main.py
Bot Anda sekarang aktif dan siap menerima perintah /start di Telegram.

Struktur Proyek
/
├── main.py                # Titik masuk utama aplikasi, inisialisasi bot dan ConversationHandler
├── config.py              # Menyimpan semua kunci API dan konfigurasi
├── requirements.txt       # Daftar semua dependensi Python
├── data.db                # Database SQLite (dibuat otomatis)
│
├── handlers/              # Modul untuk menangani interaksi pengguna
│   ├── __init__.py
│   ├── start.py           # Handler untuk perintah /start
│   ├── token_select.py    # Handler untuk pemilihan token
│   ├── timeframe_select.py# Handler untuk pemilihan timeframe
│   └── analysis.py        # Handler untuk callback analisis
│
└── utils/                 # Modul utilitas dan fungsi pembantu
    ├── __init__.py
    ├── api_helper.py      # Fungsi untuk mengambil data dari CoinGecko
    ├── ai_helper.py       # Fungsi untuk berinteraksi dengan Gemini AI
    ├── chart_helper.py    # Fungsi untuk membuat gambar chart
    ├── cooldown.py        # Logika untuk sistem cooldown
    └── db.py              # Fungsi untuk interaksi dengan database SQLite
