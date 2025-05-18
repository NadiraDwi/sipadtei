from flask import Blueprint, render_template
from models.ruang import Ruang
from koneksi import get_db_connection

ruang_bp = Blueprint('ruang', __name__)

@ruang_bp.route("/ruang", endpoint='ruang')
def ruang():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            r.kode_ruang, r.gedung, r.lantai, r.ruang, r.max_peserta,
            k.id_kategori, k.nama_kategori
        FROM ruang r
        JOIN kategori k ON r.id_kategori = k.id_kategori
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    ruang_list = []
    for row in results:
        ruang_obj = Ruang(
            kode_ruang=row['kode_ruang'],
            gedung=row['gedung'],
            lantai=row['lantai'],
            ruang=row['ruang'],
            max_peserta=row['max_peserta'],
            id_kategori=row['id_kategori'],
            nama_kategori=row['nama_kategori']
        )
        ruang_list.append(ruang_obj)

    return render_template("ruang/index.html", ruang=ruang_list)
