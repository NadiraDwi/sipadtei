# web.py
from flask import Flask
from controllers.detailmk import detailmk_bp
from controllers.kategori import kategori_bp
from controllers.ruang import ruang_bp
from controllers.offering import offering_bp
from controllers.dosen import DosenController
from controllers.mk import mk
from controllers.dashboard import DashboardController
from auth import UserController

app = Flask(__name__)
app.secret_key = 'sipadtei2025'

dashboard_controller = DashboardController()
user_controller = UserController()
dosen_controller = DosenController()

# Daftarkan semua blueprint
app.register_blueprint(user_controller.auth_bp)
app.register_blueprint(dashboard_controller.dashboard_bp)
app.register_blueprint(detailmk_bp)
app.register_blueprint(kategori_bp)
app.register_blueprint(ruang_bp)
app.register_blueprint(offering_bp)
app.register_blueprint(dosen_controller.dosen_bp)
app.register_blueprint(mk)

if __name__ == "__main__":
    app.run(debug=True)
