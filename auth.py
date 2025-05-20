import hashlib
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
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
        return admin   # <-- return admin dict, bukan True
    return None

# Halaman login
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = check_login(username, password)
        if admin:
            session['username'] = admin['username']
            session['id_admin'] = admin['id_admin']
            print("DEBUG login session:", dict(session))
            return redirect(url_for('dashboard.dashboard'))
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

class AdminManager:
    def __init__(self, id_admin):
        self.id_admin = id_admin
        self.conn = get_db_connection()

    def check_password(self, password):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM admin WHERE id_admin = %s", (self.id_admin,))
        admin = cursor.fetchone()
        cursor.close()
        if admin and hashlib.md5(password.encode()).hexdigest() == admin['password']:
            return True
        return False

    def update_password(self, new_password):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE admin SET password = %s WHERE id_admin = %s", (new_password, self.id_admin))
        self.conn.commit()
        cursor.close()
        self.conn.close()

# Route edit password
@auth_bp.route("/edit_password", methods=["GET", "POST"], endpoint='edit_password')
def edit_password():
    if 'id_admin' not in session:
        return redirect(url_for('auth.login'))

    admin_manager = AdminManager(session['id_admin'])

    if request.method == "POST":
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validasi konfirmasi password lama
        if not admin_manager.check_password(old_password):
            flash("Password lama salah.", "danger")
            return redirect(url_for('auth.edit_password'))

        # Validasi password baru dan konfirmasi
        if new_password != confirm_password:
            flash("Password baru dan konfirmasi tidak sama.", "danger")
            return redirect(url_for('auth.edit_password'))

        # Update password baru
        admin_manager.update_password(new_password)
        flash("Password berhasil diubah.", "success")
        return redirect(url_for('auth.logout'))

    return render_template("edit_password.html")