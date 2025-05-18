from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.ruang import Ruang
from models.kategori import Kategori

ruang_bp = Blueprint('ruang', __name__)

@ruang_bp.route("/ruang", endpoint='ruang')
def ruang():
    ruang_list = Ruang.semua()
    for r in ruang_list:
        print(r.kode_ruang, r.nama_kategori) 
    return render_template("ruang/index.html", ruang=ruang_list)

@ruang_bp.route("/ruang/tambah", methods=["GET", "POST"], endpoint="tambah_ruang")
def tambah_ruang():
    if request.method == "POST":
        kode_ruang = request.form.get("kode_ruang")
        gedung = request.form.get("gedung")
        lantai = request.form.get("lantai")
        ruang_nama = request.form.get("ruang")
        max_peserta = request.form.get("max_peserta")
        id_kategori = request.form.get("id_kategori")

        if not all([kode_ruang, gedung, lantai, ruang_nama, max_peserta, id_kategori]):
            flash("Semua field harus diisi!", "danger")
            return redirect(url_for("ruang.tambah_ruang"))

        # Simpan ke database (query insert langsung atau buat method simpan() di model)
        from koneksi import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ruang (kode_ruang, gedung, lantai, ruang, max_peserta, id_kategori)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (kode_ruang, gedung, lantai, ruang_nama, max_peserta, id_kategori))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Ruang berhasil ditambahkan!", "success")
        return redirect(url_for("ruang.ruang"))

    # Ambil semua kategori untuk dropdown
    kategori_list = Kategori.semua()
    return render_template("ruang/add.html", kategori=kategori_list)

@ruang_bp.route("/ruang/edit/<kode_ruang>", methods=["GET", "POST"])
def edit_ruang(kode_ruang):
    ruang_obj = Ruang.get_by_kode(kode_ruang)
    kategori_list = Kategori.semua()

    if not ruang_obj:
        flash("Data ruang tidak ditemukan!", "danger")
        return redirect(url_for("ruang.ruang"))

    if request.method == "POST":
        ruang_obj.gedung = request.form["gedung"]
        ruang_obj.lantai = request.form["lantai"]
        ruang_obj.ruang = request.form["ruang"]
        ruang_obj.max_peserta = request.form["max_peserta"]
        ruang_obj.id_kategori = request.form["id_kategori"]

        ruang_obj.update()
        flash("Ruang berhasil diperbarui", "success")
        return redirect(url_for("ruang.ruang"))

    return render_template("ruang/edit.html", ruang=ruang_obj, kategori=kategori_list)

@ruang_bp.route("/ruang/hapus/<kode_ruang>", methods=["POST"])
def hapus_ruang(kode_ruang):
    ruang_obj = Ruang.get_by_kode(kode_ruang)
    if ruang_obj:
        ruang_obj.hapus()
        flash("Ruang berhasil dihapus.", "success")
    return redirect(url_for("ruang.ruang"))