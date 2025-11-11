# ======================================================
# extensions.py — configuración global de extensiones Flask
# ======================================================

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Inicialización de extensiones
db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})  # ✅ tipo básico en memoria
