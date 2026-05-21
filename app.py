import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from flask import Flask, render_template, request
import sqlite3
import bcrypt
import log_manager as logger

app = Flask(__name__)

_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usuarios_vl.db')

def conectar_db():
    return sqlite3.connect(_DB_PATH)

with conectar_db() as conexion:
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conexion.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    email    = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        logger.warning(f"Intento de registro con campos vacíos — IP: {request.remote_addr}")
        return "Error: Campos vacíos", 400

    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (email, password) VALUES (?, ?)",
                (email, hashed)
            )
            conexion.commit()
        logger.success(f"Nuevo usuario registrado → {email}  |  IP: {request.remote_addr}")
    except Exception as e:
        logger.error(f"Fallo al registrar usuario '{email}': {e}")
        return "Error en la base de datos", 500

    return render_template('thanks.html')


@app.route('/dashboard_vl')
def admin_panel():
    logger.warning(f"Acceso al panel /dashboard_vl — IP: {request.remote_addr}")
    try:
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios")
            datos = cursor.fetchall()
        logger.info(f"Panel admin cargado — {len(datos)} registro(s) consultado(s).")
        return render_template('admin.html', usuarios=datos)
    except Exception as e:
        logger.error(f"Error en panel admin: {e}")
        return "Error en el panel", 500


if __name__ == '__main__':
    logger.iniciar_sesion()
    app.run(host='0.0.0.0', port=5000)
