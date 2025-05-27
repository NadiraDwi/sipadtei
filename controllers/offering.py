from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.offering import Offering

class OfferingController:
    def __init__(self):
        self.offering_bp = Blueprint('offering', __name__)
        self.offering_bp.add_url_rule("/offering", view_func=self.list_offering)
        self.offering_bp.add_url_rule("/offering/tambah", view_func=self.tambah_offering, methods=["GET", "POST"])
        self.offering_bp.add_url_rule("/offering/edit/<int:id>", view_func=self.edit_offering, methods=["GET", "POST"])
        self.offering_bp.add_url_rule("/offering/hapus/<int:id>", view_func=self.hapus_offering, methods=["POST"])

    def list_offering(self):
        semua_offering = Offering.semua()
        return render_template("offering/index.html", offering=semua_offering)

    def tambah_offering(self):
        if request.method == "POST":
            kode = request.form.get("kode_off")
            nama = request.form.get("nama_off")

            if not kode:
                flash("Kode offering tidak boleh kosong!", "danger")
                return redirect(url_for("offering.tambah_offering"))
        
            if not nama:
                flash("Nama offering tidak boleh kosong!", "danger")
                return redirect(url_for("offering.tambah_offering"))

            offering_baru = Offering(kode, nama)
            offering_baru.simpan()
            flash("Offering berhasil ditambahkan!", "success")
            return redirect(url_for("offering.list_offering"))

        return render_template("offering/add.html")

    def edit_offering(self, id):
        offering = Offering.cari(id)

        if not offering:
            flash("Offering tidak ditemukan!", "danger")
            return redirect(url_for("offering.list_offering"))

        if request.method == "POST":
            nama_baru = request.form.get("nama_offering", "").strip()
            if not nama_baru:
                flash("Nama offering tidak boleh kosong!", "danger")
                return redirect(url_for("offering.edit_offering", id=id))

            offering.set_nama(nama_baru)
            offering.update()
            flash("Offering berhasil diperbarui.", "success")
            return redirect(url_for("offering.list_offering"))

        return render_template("offering/edit.html", offering=offering)

    def hapus_offering(self, id):
        offering = Offering.cari(id)
        if offering:
            offering.hapus()
            flash("Offering berhasil dihapus.", "success")
        else:
            flash("Offering tidak ditemukan.", "danger")
        return redirect(url_for("offering.list_offering"))


# Inisialisasi dan expose blueprint dari kelas
offering_controller = OfferingController()
offering_bp = offering_controller.offering_bp
