import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt
import log_manager as logger

app = Flask(__name__)
_secret = os.environ.get('SECRET_KEY')
if not _secret:
    import warnings
    warnings.warn("SECRET_KEY no configurada — las sesiones se invalidarán al reiniciar. Define SECRET_KEY en el entorno.")
    _secret = 'dev-insecure-key-change-in-prod'
app.secret_key = _secret

_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usuarios_vl.db')

_ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
_ADMIN_HASH = bcrypt.hashpw(
    os.environ.get('ADMIN_PASS', 'admin123').encode('utf-8'),
    bcrypt.gensalt()
)


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
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed = hashed.decode('utf-8')
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


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == _ADMIN_USER and bcrypt.checkpw(password.encode('utf-8'), _ADMIN_HASH):
            session['admin'] = True
            logger.success(f"Login admin exitoso — IP: {request.remote_addr}")
            return redirect(url_for('admin_panel'))
        logger.warning(f"Login admin fallido (usuario: '{username}') — IP: {request.remote_addr}")
        error = "Credenciales incorrectas"
    return render_template('admin_login.html', error=error)


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    logger.info(f"Logout admin — IP: {request.remote_addr}")
    return redirect(url_for('admin_login'))


@app.route('/dashboard_vl')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    logger.warning(f"Acceso al panel /dashboard_vl — IP: {request.remote_addr}")
    q = request.args.get('q', '').strip()

    try:
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            if q:
                cursor.execute(
                    "SELECT * FROM usuarios WHERE email LIKE ?",
                    (f'%{q}%',)
                )
            else:
                cursor.execute("SELECT * FROM usuarios")
            datos = cursor.fetchall()
        logger.info(f"Panel admin cargado — {len(datos)} registro(s) consultado(s).")
        return render_template('admin.html', usuarios=datos, query=q)
    except Exception as e:
        logger.error(f"Error en panel admin: {e}")
        return "Error en el panel", 500


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    try:
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conexion.commit()
        logger.warning(f"Usuario ID {user_id} eliminado — IP: {request.remote_addr}")
    except Exception as e:
        logger.error(f"Error al eliminar usuario ID {user_id}: {e}")
        return "Error al eliminar", 500

    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    logger.iniciar_sesion()
    app.run(host='0.0.0.0', port=5000)
