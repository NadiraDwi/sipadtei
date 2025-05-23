# web.py
from flask import Flask
from auth import auth_bp
from controllers.dashboard import dashboard_bp
from controllers.detailmk import detailmk_bp
from controllers.kategori import kategori_bp
from controllers.ruang import ruang_bp
from controllers.offering import offering_bp
from controllers.dosen import dosen_bp
from controllers.mk import mk

app = Flask(__name__)
app.secret_key = 'sipadtei2025'

# Daftarkan semua blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(detailmk_bp)
app.register_blueprint(kategori_bp)
app.register_blueprint(ruang_bp)
app.register_blueprint(offering_bp)
app.register_blueprint(dosen_bp)
app.register_blueprint(mk)

if __name__ == "__main__":
    app.run(debug=True)
