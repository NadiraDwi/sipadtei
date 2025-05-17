import hashlib
from flask import Blueprint, request, render_template, redirect, url_for, session
from koneksi import get_db_connection

auth_bp = Blueprint('auth', __name__)

# Fungsi untuk cek login
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

# Halaman login
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_login(username, password):
            session['username'] = username  # Simpan username di session
            return redirect(url_for('dashboard.dashboard'))  # Ubah sesuai dengan route dashboard kamu
        else:
            return "Login Failed. Please check your credentials."

    return render_template('login.html')

# Halaman profil (ambil data dari session)
@auth_bp.route("/profile", endpoint='profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  # Arahkan ke login jika belum login

    username = session['username']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile.html', admin=admin)

# Logout (opsional)
@auth_bp.route("/logout", endpoint='logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
