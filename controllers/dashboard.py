from flask import Blueprint, render_template
from models.detail_mk import DetailMataKuliah, JadwalModel, DosenModel, RuangModel, OfferingModel
from koneksi import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard", endpoint='dashboard')
def dashboard():
    db = get_db_connection()

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