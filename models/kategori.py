from koneksi import DatabaseConnection

db = DatabaseConnection()

class Kategori:
    def __init__(self, id_kategori=None, nama_kategori=None):
        self.__id_kategori = id_kategori
        self.__nama_kategori = nama_kategori

    def info(self):
        return f"Kategori: {self.get_nama()}"

    def get_id(self):
        return self.__id_kategori

    def get_nama(self):
        return self.__nama_kategori

    def set_nama(self, nama):
        self.__nama_kategori = nama

    @staticmethod
    def semua():
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kategori")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Kategori(r['id_kategori'], r['nama_kategori']) for r in rows]

    def simpan(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO kategori (id_kategori, nama_kategori) VALUES (%s, %s)",
            (self.__id_kategori, self.__nama_kategori)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def cari(id_kategori):
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kategori WHERE id_kategori = %s", (id_kategori,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Kategori(row['id_kategori'], row['nama_kategori']) if row else None

    def update(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE kategori SET nama_kategori = %s WHERE id_kategori = %s",
            (self.__nama_kategori, self.__id_kategori)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def hapus(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kategori WHERE id_kategori = %s", (self.__id_kategori,))
        conn.commit()
        cursor.close()
        conn.close()