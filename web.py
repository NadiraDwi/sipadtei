# web.py
from flask import Flask
from auth import auth_bp
from controllers.dashboard import dashboard_bp
from controllers.detailmk import detailmk_bp
from controllers.kategori import kategori_bp
from controllers.ruang import ruang_bp

app = Flask(__name__)
app.secret_key = 'sipadtei2025'

# Daftarkan semua blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(detailmk_bp)
app.register_blueprint(kategori_bp)
app.register_blueprint(ruang_bp)

if __name__ == "__main__":
    app.run(debug=True)
