from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def conectar_db():
    return sqlite3.connect('usuarios_vl.db')

# Inicializar base de datos
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
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return "Error: Campos vacíos", 400
    try:
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (email, password) VALUES (?, ?)", (email, password))
            conexion.commit()
    except Exception as e:
        return f"Error en la base de datos: {e}", 500
    return render_template('thanks.html')

@app.route('/dashboard_vl')
def admin_panel():
    try:
        with conectar_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios")
            datos = cursor.fetchall()
        return render_template('admin.html', usuarios=datos)
    except Exception as e:
        return f"Error en el panel: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
