from koneksi import DatabaseConnection

db = DatabaseConnection()

class Offering:
    def __init__(self, id_off=None, nama_off=None):
        self.__id_off = id_off
        self.__nama_off = nama_off

    def info(self):
        return f"Offering: {self.get_nama()}"

    def get_id(self):
        return self.__id_off

    def get_nama(self):
        return self.__nama_off

    def set_nama(self, nama):
        self.__nama_off = nama

    @staticmethod
    def semua():
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM offering")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Offering(r['id_off'], r['nama_off']) for r in rows]

    def simpan(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO offering (id_off, nama_off) VALUES (%s, %s)",
            (self.__id_off, self.__nama_off)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def cari(id_off):
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM offering WHERE id_off = %s", (id_off,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Offering(row['id_off'], row['nama_off']) if row else None

    def update(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE offering SET nama_off = %s WHERE id_off = %s",
            (self.__nama_off, self.__id_off)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def hapus(self):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM offering WHERE id_off = %s", (self.__id_off,))
        conn.commit()
        cursor.close()
        conn.close()