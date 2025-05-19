from koneksi import get_db_connection

class Dosen:
    def __init__(self, nidn=None, nama_dosen=None, jabatan=None):
        self.__nidn = nidn
        self.__nama_dosen = nama_dosen
        self.__jabatan = jabatan

    def get_nidn(self):
        return self.__nidn

    def get_nama(self):
        return self.__nama_dosen

    def get_jabatan(self):
        return self.__jabatan

    def set_nama(self, nama):
        self.__nama_dosen = nama

    def set_jabatan(self, jabatan):
        self.__jabatan = jabatan

    def info(self):
        return f"Dosen: {self.get_nama()}"

    @staticmethod
    def semua():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dosen")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Dosen(r['nidn'], r['nama_dosen'], r['jabatan']) for r in rows]

    def simpan(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO dosen (nidn, nama_dosen, jabatan) VALUES (%s, %s, %s)",
            (self.__nidn, self.__nama_dosen, self.__jabatan)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def cari(nidn):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dosen WHERE nidn = %s", (nidn,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Dosen(row['nidn'], row['nama_dosen'], row['jabatan']) if row else None

    def update(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE dosen SET nama_dosen = %s, jabatan = %s WHERE nidn = %s",
            (self.__nama_dosen, self.__jabatan, self.__nidn)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def hapus(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dosen WHERE nidn = %s", (self.__nidn,))
        conn.commit()
        cursor.close()
        conn.close()