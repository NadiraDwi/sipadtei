from flask import Blueprint, render_template
from models.detail_mk import DetailMataKuliah

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard", endpoint='dashboard')
def dashboard():
    semua_mk = DetailMataKuliah.dengan_format_html()
    return render_template('index.html', mata_kuliah=semua_mk)