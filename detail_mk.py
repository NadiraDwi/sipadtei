from flask import Blueprint, render_template
from collections import defaultdict
from koneksi import get_db_connection

detailmk_bp = Blueprint('detailmk', __name__)

@detailmk_bp.route("/detailmk", endpoint='detailmk')
def detail_mk():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detail_mk")  # Tetap gunakan view yang kamu buat
    rows = cursor.fetchall()
    db.close()

    grouped = {}

    for row in rows:
        kode_mk = row['kode_mk']
        if kode_mk not in grouped:
            # Buat entry baru jika belum ada
            grouped[kode_mk] = {
                'kode_mk': row['kode_mk'],
                'mata_kuliah': row['mata_kuliah'],
                'kategori': row['kategori'],
                'offering': row['offering'],
                'hari': row['hari'],
                'jam_awal': row['jam_awal'],
                'jam_akhir': row['jam_akhir'],
                'kode_ruang': row['kode_ruang'],
                'max_peserta': row['max_peserta'],
                'jml_peserta': row['jml_peserta'],
                'admin': row['admin'],
                'dosen_list': [row['dosen']]
            }
        else:
            # Kalau sudah ada, tambahkan dosennya
            grouped[kode_mk]['dosen_list'].append(row['dosen'])

    # Siapkan list akhir dengan dosen digabung koma (tanpa duplikat)
    result = []
    for mk in grouped.values():
        mk['dosen'] = ', '.join(sorted(set(mk['dosen_list'])))
        del mk['dosen_list']
        result.append(mk)

    return render_template('detail_mk.html', mata_kuliah=result)
