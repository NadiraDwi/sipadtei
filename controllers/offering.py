from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.offering import Offering

offering_bp = Blueprint('offering', __name__)

@offering_bp.route("/offering")
def offering():
    semua_offering = Offering.semua()
    return render_template("offering/index.html", offering=semua_offering)

@offering_bp.route("/offering/tambah", methods=["GET", "POST"])
def tambah_offering(offering):
    if request.method == "POST":
        kode = request.form.get("kode_off")
        nama = request.form.get("nama_off")

        if not kode:
            flash("Nama kategori tidak boleh kosong!", "danger")
            return redirect(url_for("kategori.tambah_offering"))
    
        if not nama:
            flash("Nama kategori tidak boleh kosong!", "danger")
            return redirect(url_for("kategori.tambah_offering"))

        offering_baru = Offering(kode, nama)
        offering_baru.simpan()
        flash("Offering berhasil ditambahkan!", "success")
        return redirect(url_for("offering.offering"))

    return render_template("offering/add.html")

@offering_bp.route("/offering/edit/<id>", methods=["GET", "POST"])
def edit_offering(id):
    offering = Offering.cari(id)

    if not offering:
        flash("Offering tidak ditemukan!", "danger")
        return redirect(url_for("offering.offering"))

    if request.method == "POST":
        nama_baru = request.form["nama_offering"]
        offering.set_nama(nama_baru)
        offering.update()
        flash("Offering berhasil diperbarui.", "success")
        return redirect(url_for("offering.offering"))

    return render_template("offering/edit.html", offering=offering)

@offering_bp.route("/offering/hapus/<id>", methods=["POST"])
def hapus_offering(id):
    offering = Offering.cari(id)
    if Offering:
        offering.hapus()
        flash("Offering berhasil dihapus.", "success")
    return redirect(url_for("offering.offering"))
