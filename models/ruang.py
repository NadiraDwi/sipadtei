from models.kategori import Kategori
from koneksi import get_db_connection

class Ruang(Kategori):
    def __init__(self, kode_ruang, gedung, lantai, ruang, max_peserta, id_kategori, nama_kategori):
        # Panggil constructor superclass (Kategori)
        super().__init__(id_kategori, nama_kategori)
        
        self.kode_ruang = kode_ruang
        self.gedung = gedung
        self.lantai = lantai
        self.ruang = ruang
        self.max_peserta = max_peserta
        
        # Tambahkan atribut publik agar mudah diakses
        self.id_kategori = id_kategori
        self.nama_kategori = nama_kategori

    def info(self):      # overriding method info()
        return f"Ruang {self.ruang} - Kategori: {self.get_nama()}"
    
    def to_dict(self):
        return {
            "kode_ruang": self.kode_ruang,
            "gedung": self.gedung,
            "lantai": self.lantai,
            "ruang": self.ruang,
            "max_peserta": self.max_peserta,
            "id_kategori": self.id_kategori,
            "nama_kategori": self.nama_kategori
        }

    @staticmethod
    def semua():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.kode_ruang, r.gedung, r.lantai, r.ruang, r.max_peserta,
                   k.id_kategori, k.nama_kategori
            FROM ruang r
            JOIN kategori k ON r.id_kategori = k.id_kategori
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        ruang_list = []
        for row in rows:
            ruang = Ruang(
                kode_ruang=row['kode_ruang'],
                gedung=row['gedung'],
                lantai=row['lantai'],
                ruang=row['ruang'],
                max_peserta=row['max_peserta'],
                id_kategori=row['id_kategori'],
                nama_kategori=row['nama_kategori']
            )
            ruang_list.append(ruang)

        return ruang_list

    @staticmethod
    def get_by_kode(kode_ruang):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, k.nama_kategori 
            FROM ruang r JOIN kategori k ON r.id_kategori = k.id_kategori 
            WHERE r.kode_ruang = %s
        """, (kode_ruang,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Ruang(
                kode_ruang=row['kode_ruang'],
                gedung=row['gedung'],
                lantai=row['lantai'],
                ruang=row['ruang'],
                max_peserta=row['max_peserta'],
                id_kategori=row['id_kategori'],
                nama_kategori=row['nama_kategori']
            )
        return None

    def update(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ruang SET gedung=%s, lantai=%s, ruang=%s, max_peserta=%s, id_kategori=%s 
            WHERE kode_ruang = %s
        """, (self.gedung, self.lantai, self.ruang, self.max_peserta, self.id_kategori, self.kode_ruang))
        conn.commit()
        cursor.close()
        conn.close()

    def hapus(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ruang WHERE kode_ruang = %s", (self.kode_ruang,))
        conn.commit()
        cursor.close()
        conn.close()