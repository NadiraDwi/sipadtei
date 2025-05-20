from koneksi import get_db_connection

class DetailMataKuliah:
    def __init__(self, data):
        self.__kode_mk = data['kode_mk']
        self.__mata_kuliah = data['mata_kuliah']
        self.__kategori = data['kategori']
        self.__offering = data['offering']
        self.__hari = data['hari']
        self.__jam_awal = data['jam_awal']
        self.__jam_akhir = data['jam_akhir']
        self.__kode_ruang = data['kode_ruang']
        self.__max_peserta = data['max_peserta']
        self.__jml_peserta = data['jml_peserta']
        self.__admin = data['admin']
        self.__dosen_list = [data['dosen']]

    def get_kode_mk(self): return self.__kode_mk
    def get_mata_kuliah(self): return self.__mata_kuliah
    def get_kategori(self): return self.__kategori
    def get_offering(self): return self.__offering
    def get_hari(self): return self.__hari
    def get_jam_awal(self): return self.__jam_awal
    def get_jam_akhir(self): return self.__jam_akhir
    def get_kode_ruang(self): return self.__kode_ruang
    def get_max_peserta(self): return self.__max_peserta
    def get_jml_peserta(self): return self.__jml_peserta
    def get_admin(self): return self.__admin
    def get_dosen_list(self): return self.__dosen_list

    def tambah_dosen(self, nama):
        if nama not in self.__dosen_list:
            self.__dosen_list.append(nama)

    def to_dict(self):
        return {
            'kode_mk': self.__kode_mk,
            'mata_kuliah': self.__mata_kuliah,
            'kategori': self.__kategori,
            'offering': self.__offering,
            'hari': self.__hari,
            'jam_awal': self.__jam_awal,
            'jam_akhir': self.__jam_akhir,
            'kode_ruang': self.__kode_ruang,
            'max_peserta': self.__max_peserta,
            'jml_peserta': self.__jml_peserta,
            'admin': self.__admin,
            'dosen': ', '.join(sorted(set(self.__dosen_list)))
        }

    @staticmethod
    def semua():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detail_mk")
        rows = cursor.fetchall()
        conn.close()

        mk_dict = {}
        for row in rows:
            kode = row['kode_mk']
            if kode not in mk_dict:
                mk_dict[kode] = DetailMataKuliah(row)
            else:
                mk_dict[kode].tambah_dosen(row['dosen'])

        return [mk.to_dict() for mk in mk_dict.values()]

    @staticmethod
    def cari_by_kode(kode_mk):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detail_mk WHERE kode_mk = %s", (kode_mk,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return None

        mk = DetailMataKuliah(rows[0])
        for row in rows[1:]:
            mk.tambah_dosen(row['dosen'])

        return mk.to_dict()

    @staticmethod
    def dengan_format_html():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detail_mk")
        rows = cursor.fetchall()
        conn.close()

        mk_dict = {}
        for row in rows:
            kode = row['kode_mk']
            if kode not in mk_dict:
                mk_dict[kode] = DetailMataKuliah(row)
            else:
                mk_dict[kode].tambah_dosen(row['dosen'])

        hasil = []
        for mk in mk_dict.values():
            data = mk.to_dict()
            data['dosen'] = ',<br> '.join(sorted(set(mk.get_dosen_list())))
            hasil.append(data)

        return hasil
    
class BaseModel:
    def __init__(self, db):
        self.db = db

    def get_total(self):
        """Method default, akan dioverride oleh child class."""
        raise NotImplementedError("Subclasses must implement this method.")

class JadwalModel(BaseModel):
    def get_total(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM jadwal")
        result = cursor.fetchone()
        cursor.close()
        return {
            "nama": "Jadwal",
            "total": result[0] if result else 0
        }

class DosenModel(BaseModel):
    def get_total(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM dosen")
        result = cursor.fetchone()
        cursor.close()
        return {
            "nama": "Dosen",
            "total": result[0] if result else 0
        }
class RuangModel(BaseModel):
    def get_total(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM ruang")
        result = cursor.fetchone()
        cursor.close()
        return {
            "nama": "Ruang",
            "total": result[0] if result else 0
        }

class OfferingModel(BaseModel):
    def get_total(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM offering")
        result = cursor.fetchone()
        cursor.close()
        return {
            "nama": "Offering",
            "total": result[0] if result else 0
        }
