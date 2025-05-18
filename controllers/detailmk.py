from flask import Blueprint, render_template
from models.detail_mk import DetailMataKuliah

detailmk_bp = Blueprint('detailmk', __name__)

@detailmk_bp.route("/detailmk", endpoint='detailmk')
def detail_mk():
    semua_mk = DetailMataKuliah.semua()
    return render_template('detail_mk.html', mata_kuliah=semua_mk)
