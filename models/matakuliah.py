from koneksi import get_db_connection

class MatakuliahModel:
    def __init__(self, db):
        self.db = db
        self.__kode_mk = None  # disiapkan untuk penyimpanan kode MK secara internal

    def set_kode_mk(self, kode_mk):
        """Setter kode MK untuk digunakan dalam metode hapus."""
        self.__kode_mk = kode_mk

    def get_detail(self, kode_mk):
        cursor = self.db.cursor(dictionary=True)
        sql = """
           SELECT
                m.kode_mk, m.mata_kuliah, k.nama_kategori AS kategori,
                GROUP_CONCAT(d.nama_dosen SEPARATOR ', ') AS dosen_names,
                GROUP_CONCAT(d.nidn SEPARATOR ', ') AS dosen_nidns,
                m.id_off AS offering,
                j.hari, j.jam_awal, j.jam_akhir,
                r.kode_ruang, m.jml_peserta,
                a.nama AS admin
            FROM matakuliah m
            JOIN kategori k ON m.id_kategori = k.id_kategori
            JOIN offering o ON o.id_off = m.id_off
            JOIN jadwal j ON j.id_jadwal = m.id_jadwal
            JOIN ruang r ON r.kode_ruang = j.kode_ruang
            JOIN admin a ON a.id_admin = m.id_admin
            LEFT JOIN dosen_mk dmk ON dmk.kode_mk = m.kode_mk
            LEFT JOIN dosen d ON d.nidn = dmk.nidn
            WHERE m.kode_mk = %s
            GROUP BY m.kode_mk

        """
        cursor.execute(sql, (kode_mk,))
        result = cursor.fetchone()
        cursor.close()

        self.set_kode_mk(kode_mk)
        return result
    
    def simpan(self, data):
        try:
            cursor = self.db.cursor()
            cursor.callproc('tambah_matakuliah_validasi', [
                data['kode_mk'], data['mata_kuliah'], data['id_kategori'], data['id_off'],
                data['hari'], data['jam_awal'], data['jam_akhir'], data['kode_ruang'],
                int(data['jml_peserta']), data['id_admin']
            ])

            for nidn in data['nidn_list']:
                cursor.execute("""
                    INSERT INTO dosen_mk (kode_mk, nidn)
                    VALUES (%s, %s)
                """, (data['kode_mk'], nidn))

            self.db.commit()
            cursor.close()
            return True, None

        except Exception as e:
            self.db.rollback()
            error_msg = str(e)
            print(f"Error saat simpan matakuliah: {error_msg}")
            return False, error_msg

    def edit(self, data):
        try:
            cursor = self.db.cursor()

            # Panggil stored procedure edit_matakuliah
            cursor.callproc('edit_matakuliah', [
                data['kode_mk'], data['mata_kuliah'], data['id_kategori'], data['id_off'],
                data['hari'], data['jam_awal'], data['jam_akhir'], data['kode_ruang'],
                int(data['jml_peserta']), data['id_admin']
            ])

            # Hapus dulu dosen lama untuk kode_mk ini
            cursor.execute("DELETE FROM dosen_mk WHERE kode_mk = %s", (data['kode_mk'],))

            # Tambahkan dosen baru dari daftar
            for nidn in data['nidn_list']:
                cursor.execute("""
                    INSERT INTO dosen_mk (kode_mk, nidn)
                    VALUES (%s, %s)
                """, (data['kode_mk'], nidn))

            self.db.commit()
            cursor.close()
            return True, None

        except Exception as e:
            self.db.rollback()
            error_msg = str(e)
            print(f"Error saat edit matakuliah: {error_msg}")
            return False, error_msg

    def hapus(self):
        if not self.__kode_mk:
            raise ValueError("kode_mk belum diset. Pastikan get_detail() dipanggil dulu atau set_kode_mk() digunakan.")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Panggil stored procedure dengan parameter kode_mk
        cursor.callproc("hapus_matakuliah", [self.__kode_mk])

        conn.commit()
        cursor.close()
        conn.close()
