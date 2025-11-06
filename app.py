# ======================================================
# app.py — versión FINAL y sincronizada (hora local Chile 🇨🇱)
# ======================================================

import os
from functools import wraps
from flask import Flask, session, redirect, url_for, flash
from flask_migrate import Migrate
from extensions import db

# ---------------------------
# ⏰ Importar módulo de tiempo centralizado
# ---------------------------
from tiempo import hora_actual, to_hora_chile as hora_chile  # ✅ hora real Chile

# ======================================================
# 🚀 Inicialización de la app
# ======================================================
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET", "clave_secreta_local_cámbiala")

# ======================================================
# 🕒 Registrar funciones globales para Jinja (uso en HTML)
# ======================================================
# 🔹 Permite usar {{ hora_actual() }}, {{ hora_chile() }} y el filtro |hora_chile
app.jinja_env.globals.update(hora_actual=hora_actual)
app.jinja_env.filters["hora_chile"] = hora_chile
app.jinja_env.globals.update(hora_chile=hora_chile)

# ======================================================
# ⚙️ Configuración de la base de datos (Neon)
# ======================================================

# 🔗 Cadena directa de conexión Neon (una sola línea, tal como la entrega Neon)
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_W6kO3HxNzudU@ep-round-shape-a462zq46-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 🔁 Compatibilidad Render (por si en el futuro usas su variable de entorno)
env_url = os.getenv("DATABASE_URL")
if env_url and env_url != "":
    DATABASE_URL = env_url.replace("postgres://", "postgresql://", 1)

# Configuración de SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ======================================================
# 🔐 LOGIN Y SESIÓN
# ======================================================
app.config["VALID_USER"] = "carmensmm"
app.config["VALID_PASS"] = "wendy67"

def login_required(f):
    """Decorador para proteger rutas que requieren sesión activa."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("rutas.login"))
        return f(*args, **kwargs)
    return wrapper

# ======================================================
# 🔗 Registro de rutas (Blueprint principal)
# ======================================================
from rutas import app_rutas
app.register_blueprint(app_rutas)

# ======================================================
# 📦 Inicializar extensiones
# ======================================================
db.init_app(app)
migrate = Migrate(app, db)

# ======================================================
# 🗃️ Crear tablas si no existen
# ======================================================
with app.app_context():
    db.create_all()

# ======================================================
# ▶️ Punto de entrada
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)
