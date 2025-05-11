import hashlib
from flask import Blueprint, request, render_template, redirect, url_for
from koneksi import get_db_connection

auth_bp = Blueprint('auth', __name__)

def check_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if admin and hashlib.md5(password.encode()).hexdigest() == admin['password']:
        return True
    return False

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_login(username, password):
            return redirect(url_for('dashboard.dashboard'))  # dashboard di web.py
        else:
            return "Login Failed. Please check your credentials."

    return render_template('login.html')
