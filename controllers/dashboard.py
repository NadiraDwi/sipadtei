from flask import Blueprint, render_template
from models.detail_mk import DetailMataKuliah, JadwalModel, DosenModel, RuangModel, OfferingModel
from koneksi import DatabaseConnection

db = DatabaseConnection()

class DashboardController:
    def __init__(self):
        self.db = db
        self.dashboard_bp = Blueprint('dashboard', __name__)
        self.dashboard_bp.add_url_rule("/dashboard", endpoint='dashboard', view_func=self.dashboard)

    def dashboard(self):
        db = self.db.connect()

        semua_mk = DetailMataKuliah.dengan_format_html()

        jadwal_model = JadwalModel(db)
        total_jadwal = jadwal_model.get_total()

        dosen_model = DosenModel(db)
        total_dosen = dosen_model.get_total()

        ruang_model = RuangModel(db)
        total_ruang = ruang_model.get_total()

        offering_model = OfferingModel(db)
        total_offering = offering_model.get_total()

        return render_template('index.html', mata_kuliah=semua_mk, t_jadwal=total_jadwal, t_dosen=total_dosen, t_ruang=total_ruang, t_offering=total_offering)
