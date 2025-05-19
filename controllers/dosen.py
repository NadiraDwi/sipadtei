from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.dosen import Dosen

dosen_bp = Blueprint('dosen', __name__)

@dosen_bp.route("/dosen")
def dosen():
    semua_dosen = Dosen.semua()
    return render_template("dosen/index.html", dosen=semua_dosen)

@dosen_bp.route("/dosen/tambah", methods=["GET", "POST"])
def tambah_dosen():
    if request.method == "POST":
        nidn = request.form.get("nidn")
        nama = request.form.get("nama_dosen")
        jabatan = request.form.get("jabatan")

        if not nidn:
            flash("NIDN tidak boleh kosong!", "danger")
            return redirect(url_for("dosen.tambah_dosen"))
        if not nama:
            flash("Nama dosen tidak boleh kosong!", "danger")
            return redirect(url_for("dosen.tambah_dosen"))
        if not jabatan:
            flash("Jabatan dosen tidak boleh kosong!", "danger")
            return redirect(url_for("dosen.tambah_dosen"))
        
        dosen_baru = Dosen(nidn, nama, jabatan)
        dosen_baru.simpan()
        flash("Dosen berhasil ditambahkan!", "success")
        return redirect(url_for("dosen.dosen"))

    return render_template("dosen/add.html")

@dosen_bp.route("/dosen/edit/<id>", methods=["GET", "POST"])
def edit_dosen(id):
    dosen = Dosen.cari(id)

    if not dosen:
        flash("Dosen tidak ditemukan!", "danger")
        return redirect(url_for("dosen.dosen"))

    if request.method == "POST":
        nama_baru = request.form["nama_dosen"]
        jabatan_baru = request.form["jabatan"]
        dosen.set_nama(nama_baru)
        dosen.set_jabatan(jabatan_baru)
        dosen.update()
        flash("Dosen berhasil diperbarui.", "success")
        return redirect(url_for("dosen.dosen"))

    return render_template("dosen/edit.html", dosen=dosen)

@dosen_bp.route("/dosen/hapus/<id>", methods=["POST"])
def hapus_dosen(id):
    dosen = Dosen.cari(id)
    if dosen:
        dosen.hapus()
        flash("Dosen berhasil dihapus.", "success")
    return redirect(url_for("dosen.dosen"))
