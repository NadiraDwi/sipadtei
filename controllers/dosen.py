from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.dosen import Dosen

class DosenController:
    def __init__(self):
        self.dosen_bp = Blueprint('dosen', __name__)
        self.dosen_bp.add_url_rule("/dosen", view_func=self.dosen)
        self.dosen_bp.add_url_rule("/dosen/tambah", methods=["GET", "POST"], view_func=self.tambah_dosen)
        self.dosen_bp.add_url_rule("/dosen/edit/<id>", methods=["GET", "POST"], view_func=self.edit_dosen)
        self.dosen_bp.add_url_rule("/dosen/hapus/<id>", methods=["POST"], view_func=self.hapus_dosen)

    def dosen(self):
        semua_dosen = Dosen.semua()
        return render_template("dosen/index.html", dosen=semua_dosen)

    def tambah_dosen(self):
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

    def edit_dosen(self, id):
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

    def hapus_dosen(self, id):
        dosen = Dosen.cari(id)
        if dosen:
            dosen.hapus()
            flash("Dosen berhasil dihapus.", "success")
        return redirect(url_for("dosen.dosen"))
