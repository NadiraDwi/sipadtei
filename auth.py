import hashlib
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from koneksi import DatabaseConnection

db = DatabaseConnection()
class AdminManager:
    def __init__(self, id_admin):
        self._id_admin = id_admin
        self._conn = db.connect()

    def check_password(self, password):
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM admin WHERE id_admin = %s", (self._id_admin,))
        admin = cursor.fetchone()
        cursor.close()
        if admin and hashlib.md5(password.encode()).hexdigest() == admin['password']:
            return True
        return False

    def update_password(self, new_password):
        cursor = self._conn.cursor()
        cursor.execute("UPDATE admin SET password = %s WHERE id_admin = %s", (new_password, self._id_admin))
        self._conn.commit()
        cursor.close()
        self._conn.close()

class UserController:
    def __init__(self):
        self.auth_bp = Blueprint('auth', __name__)
        self.auth_bp.add_url_rule("/", methods=["GET", "POST"], view_func=self.login)
        self.auth_bp.add_url_rule("/profile", endpoint='profile', view_func=self.profile)
        self.auth_bp.add_url_rule("/logout", endpoint='logout', view_func=self.logout)
        self.auth_bp.add_url_rule("/edit_password", methods=["GET", "POST"], endpoint='edit_password', view_func=self.edit_password)

    def check_login(self, username, password):
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin and hashlib.md5(password.encode()).hexdigest() == admin['password']:
            return admin
        return None

    def login(self):
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            admin = self.check_login(username, password)
            if admin:
                session['username'] = admin['username']
                session['id_admin'] = admin['id_admin']
                print("DEBUG login session:", dict(session))
                return redirect(url_for('dashboard.dashboard'))
            else:
                return "Login Failed. Please check your credentials."

        return render_template('login.html')

    def profile(self):
        if 'username' not in session:
            return redirect(url_for('auth.login'))

        username = session['username']
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template('profile.html', admin=admin)

    def logout(self):
        session.pop('username', None)
        session.pop('id_admin', None)
        return redirect(url_for('auth.login'))

    def edit_password(self):
        if 'id_admin' not in session:
            return redirect(url_for('auth.login'))

        admin_manager = AdminManager(session['id_admin'])

        if request.method == "POST":
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not admin_manager.check_password(old_password):
                flash("Password lama salah.", "danger")
                return redirect(url_for('auth.edit_password'))

            if new_password != confirm_password:
                flash("Password baru dan konfirmasi tidak sama.", "danger")
                return redirect(url_for('auth.edit_password'))

            admin_manager.update_password(new_password)
            flash("Password berhasil diubah.", "success")
            return redirect(url_for('auth.logout'))

        return render_template("edit_password.html")
