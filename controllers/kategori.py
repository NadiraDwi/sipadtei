from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.kategori import Kategori

kategori_bp = Blueprint('kategori', __name__)

@kategori_bp.route("/kategori")
def kategori():
    semua_kategori = Kategori.semua()
    return render_template("kategori/index.html", kategori=semua_kategori)

@kategori_bp.route("/kategori/tambah", methods=["GET", "POST"])
def tambah_kategori():
    if request.method == "POST":
        nama = request.form.get("nama_kategori")

        if not nama:
            flash("Nama kategori tidak boleh kosong!", "danger")
            return redirect(url_for("kategori.tambah_kategori"))

        # Buat ID baru
        semua = Kategori.semua()
        last_id = semua[-1].get_id() if semua else "K000"
        number = int(last_id[1:]) + 1
        new_id = f"K{number:03d}"

        kategori_baru = Kategori(new_id, nama)
        kategori_baru.simpan()
        flash("Kategori berhasil ditambahkan!", "success")
        return redirect(url_for("kategori.kategori"))

    return render_template("kategori/add.html")

@kategori_bp.route("/kategori/edit/<id>", methods=["GET", "POST"])
def edit_kategori(id):
    kategori = Kategori.cari(id)

    if not kategori:
        flash("Kategori tidak ditemukan!", "danger")
        return redirect(url_for("kategori.kategori"))

    if request.method == "POST":
        nama_baru = request.form["nama_kategori"]
        kategori.set_nama(nama_baru)
        kategori.update()
        flash("Kategori berhasil diperbarui.", "success")
        return redirect(url_for("kategori.kategori"))

    return render_template("kategori/edit.html", kategori=kategori)

@kategori_bp.route("/kategori/hapus/<id>", methods=["POST"])
def hapus_kategori(id):
    kategori = Kategori.cari(id)
    if kategori:
        kategori.hapus()
        flash("Kategori berhasil dihapus.", "success")
    return redirect(url_for("kategori.kategori"))
