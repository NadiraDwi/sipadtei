import hashlib
from flask import Blueprint, request, render_template, redirect, url_for
from koneksi import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard", endpoint='dashboard')
def dashboard():
    return render_template('index.html')
