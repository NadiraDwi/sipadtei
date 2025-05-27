from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.detail_mk import DetailMataKuliah
from models.matakuliah import MatakuliahModel
from models.dosen import Dosen
from models.kategori import Kategori
from models.offering import Offering
from models.ruang import Ruang
from koneksi import DatabaseConnection

class MatakuliahController:
    def __init__(self):
        self.db = DatabaseConnection()
        self.mk = Blueprint('mk', __name__, url_prefix='/mk')

        self.mk.add_url_rule('/detail/<kode_mk>', view_func=self.detail_mk)
        self.mk.add_url_rule('/hapus/<kode_mk>', view_func=self.hapus_matakuliah, methods=['POST'])
        self.mk.add_url_rule('/tambah', view_func=self.tambah_matakuliah, methods=['GET', 'POST'])
        self.mk.add_url_rule('/edit/<kode_mk>', view_func=self.edit_mk, methods=['GET', 'POST'])

    def detail_mk(self, kode_mk):
        detail = DetailMataKuliah.cari_by_kode(kode_mk)
        if not detail:
            return "Data tidak ditemukan", 404
        return render_template('mk/detail.html', detail=detail)

    def hapus_matakuliah(self, kode_mk):
        conn = self.db.connect()
        try:
            matkul_obj = MatakuliahModel(conn)
            matkul_obj.set_kode_mk(kode_mk)
            matkul_obj.hapus()
            flash("Mata kuliah berhasil dihapus.", "success")
        except Exception as e:
            flash(f"Error hapus mata kuliah: {e}", "danger")
        finally:
            conn.close()
        return redirect(url_for("dashboard.dashboard"))

    def tambah_matakuliah(self):
        print("DEBUG tambah_matakuliah session:", dict(session))
        if request.method == 'POST':
            data = {
                'kode_mk': request.form.get('kode_mk', '').strip(),
                'mata_kuliah': request.form.get('mata_kuliah', '').strip(),
                'id_kategori': request.form.get('id_kategori', '').strip(),
                'nidn_list': request.form.getlist('nidn[]'),
                'id_off': request.form.get('id_off', '').strip(),
                'hari': request.form.get('hari', '').strip(),
                'jam_awal': request.form.get('jam_awal', '').strip(),
                'jam_akhir': request.form.get('jam_akhir', '').strip(),
                'kode_ruang': request.form.get('kode_ruang', '').strip(),
                'jml_peserta': request.form.get('jml_peserta', '').strip(),
                'id_admin': session.get('id_admin')
            }
            print("DEBUG - id_admin dari session:", data['id_admin'])

            # Validasi wajib isi
            if not data['kode_mk'] or not data['mata_kuliah']:
                flash("Kode MK dan Mata Kuliah wajib diisi.", "danger")

            elif not (data['jam_awal'].isdigit() and data['jam_akhir'].isdigit()):
                flash("Jam awal dan jam akhir harus berupa angka.", "danger")

            else:
                jam_awal = int(data['jam_awal'])
                jam_akhir = int(data['jam_akhir'])

                if jam_awal < 1 or jam_akhir > 10:
                    flash("Jam harus antara 1 sampai 10.", "danger")
                elif jam_awal >= jam_akhir:
                    flash("Jam awal harus kurang dari jam akhir.", "danger")
                else:
                    conn = None
                    try:
                        conn = self.db.connect()
                        matkul_obj = MatakuliahModel(conn)
                        success, error_msg = matkul_obj.simpan(data)
                        if success:
                            flash("Mata Kuliah berhasil ditambahkan.", "success")
                            return redirect(url_for('dashboard.dashboard'))
                        else:
                            flash(f"Terjadi kesalahan: {error_msg}", "danger")
                    except Exception as ex:
                        flash(f"Error koneksi database: {ex}", "danger")
                    finally:
                        if conn:
                            conn.close()

        return render_template(
            'mk/add.html',
            dosen=Dosen.semua(),
            kategori=Kategori.semua(),
            ruang=Ruang.semua(),
            offering=Offering.semua(),
            hari=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
        )

    def edit_mk(self, kode_mk):
        conn = self.db.connect()
        matkul_obj = MatakuliahModel(conn)
        detail = matkul_obj.get_detail(kode_mk)

        if not detail:
            flash("Data matakuliah tidak ditemukan.", "danger")
            conn.close()
            return redirect(url_for("dashboard.dashboard"))

        if request.method == 'POST':
            data = {
                'kode_mk': kode_mk,
                'mata_kuliah': request.form.get('mata_kuliah', '').strip(),
                'id_kategori': request.form.get('id_kategori', '').strip(),
                'nidn_list': request.form.getlist('nidn[]'),
                'id_off': request.form.get('id_off', '').strip(),
                'hari': request.form.get('hari', '').strip(),
                'jam_awal': request.form.get('jam_awal', '').strip(),
                'jam_akhir': request.form.get('jam_akhir', '').strip(),
                'kode_ruang': request.form.get('kode_ruang', '').strip(),
                'jml_peserta': request.form.get('jml_peserta', '').strip(),
                'id_admin': session.get('id_admin')
            }

            if not data['mata_kuliah']:
                flash("Nama Mata Kuliah wajib diisi.", "danger")
            elif not (data['jam_awal'].isdigit() and data['jam_akhir'].isdigit()):
                flash("Jam awal dan akhir harus berupa angka.", "danger")
            else:
                jam_awal = int(data['jam_awal'])
                jam_akhir = int(data['jam_akhir'])

                if jam_awal < 1 or jam_akhir > 10:
                    flash("Jam harus antara 1 sampai 10.", "danger")
                elif jam_awal >= jam_akhir:
                    flash("Jam awal harus kurang dari jam akhir.", "danger")
                else:
                    try:
                        success, error_msg = matkul_obj.edit(data)
                        if success:
                            flash("Data matakuliah berhasil diperbarui.", "success")
                            conn.close()
                            return redirect(url_for('dashboard.dashboard'))
                        else:
                            flash(f"Gagal update: {error_msg}", "danger")
                    except Exception as ex:
                        flash(f"Error koneksi database: {ex}", "danger")
                    finally:
                        conn.close()

            if not conn._closed:
                conn.close()
        else:
            conn.close()

        return render_template(
            'mk/edit.html',
            detail=detail,
            dosen=Dosen.semua(),
            kategori=Kategori.semua(),
            ruang=Ruang.semua(),
            offering=Offering.semua(),
            hari=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
        )

# Inisialisasi controller dan blueprint
matakuliah_controller = MatakuliahController()
mk = matakuliah_controller.mk
