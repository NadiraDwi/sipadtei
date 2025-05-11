import mysql.connector

# Konfigurasi koneksi ke database MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',      # Ganti dengan host MySQL kamu
        user='root',  # Ganti dengan username MySQL kamu
        password='',  # Ganti dengan password MySQL kamu
        database='sipadtei_db' # Ganti dengan nama database kamu
    )