from flask import Blueprint, render_template
from koneksi import get_db_connection

detailmk_bp = Blueprint('detailmk', __name__)

@detailmk_bp.route("/detailmk", endpoint='detailmk')
def detail_mk():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detail_mk")
    data = cursor.fetchall()
    db.close() 
    return render_template('detail_mk.html', mata_kuliah=data)