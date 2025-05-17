# web.py
from flask import Flask
from auth import auth_bp
from dashboard import dashboard_bp
from detail_mk import detailmk_bp

app = Flask(__name__)
app.secret_key = 'sipadtei2025'

# Daftarkan semua blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(detailmk_bp)

if __name__ == "__main__":
    app.run(debug=True)
