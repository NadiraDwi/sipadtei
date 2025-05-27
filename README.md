# SIPADTEI

SIPADTEI (Sistem Informasi Pengelolaan Data Mata Kuliah dan Admin) adalah aplikasi web berbasis Python dengan framework Flask yang dirancang untuk membantu pengelolaan data akademik, seperti mata kuliah, jadwal, ruang, dan data admin di lingkungan perguruan tinggi.

## 📌 Fitur Utama

- Autentikasi login admin
- Manajemen data Mata Kuliah (CRUD)
- Manajemen Kategori, Offering, Jadwal, Ruang, dan Dosen
- Relasi antar tabel dengan Foreign Key
- Fitur ubah password dengan validasi (menggunakan konsep OOP dan enkapsulasi)
- Trigger MySQL untuk hashing password dan menjaga referensialitas data

## 🛠️ Teknologi yang Digunakan

- **Python 3.x**
- **Flask** (micro web framework)
- **MySQL** (sebagai sistem basis data)
- **HTML5, CSS3, Bootstrap, AdminLTE** (untuk tampilan antarmuka)
- **Blueprint Flask** untuk modularisasi
- **MVC Pattern** (Model-View-Controller)

## 🧱 Struktur Basis Data

Basis data terdiri dari beberapa tabel utama:
- `admin`: menyimpan data login dan identitas admin
- `matakuliah`: menyimpan data mata kuliah
- `kategori`: jenis kategori mata kuliah
- `offering`: data penawaran/program studi
- `dosen`: data dosen pengajar
- `jadwal`: jadwal kelas
- `ruang`: data ruang kelas
- `dosen_mk`: relasi antara dosen dan mata kuliah

Relasi antar tabel sudah didesain menggunakan kunci primer dan kunci asing untuk menjaga konsistensi data.

## 🖥️ Cara Menjalankan Aplikasi

1. Clone repository:
   ```bash
   git clone https://github.com/NadiraDwi/sipadtei.git
   cd sipadtei
2. Install dependencies (gunakan virtual environment jika perlu):
    ```bash
    pip install Flask mysql-connector-python

3. Buat database bernama sipadtei
    Import file SQL jika tersedia (pastikan struktur tabel sesuai)
    Konfigurasi koneksi database di file koneksi.py:
    ```bash
    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="sipadtei"
        )
4. Jalankan aplikasi:
    ```bash
    python web.py
    
5. Akses aplikasi melalui browser:
    ```bash
    http://localhost:5000
