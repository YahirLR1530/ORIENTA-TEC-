import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect('estadisticas_kiosco.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS interacciones 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, seccion TEXT, fecha TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sesiones 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, inicio TEXT, fin TEXT, 
                       duracion_segundos REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/click/<seccion>')
def registrar_click(seccion):
    try:
        conn = sqlite3.connect('estadisticas_kiosco.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO interacciones (seccion, fecha) VALUES (?, ?)", 
                       (seccion, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/sesion/guardar/<inicio>/<fin>/<duracion>')
def guardar_sesion(inicio, fin, duracion):
    try:
        conn = sqlite3.connect('estadisticas_kiosco.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sesiones (inicio, fin, duracion_segundos) VALUES (?, ?, ?)",
                       (inicio, fin, float(duracion)))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- MODIFICACIÓN PARA DESPLIEGUE EN LA NUBE ---
if __name__ == "__main__":
    init_database()
    
    # Render asigna un puerto automáticamente en la variable de entorno 'PORT'.
    # Si corres el código en tu compu local, usará el puerto 5000 por defecto.
    port = int(os.environ.get("PORT", 5000))
    
    # Quitamos el modo debug=True para producción en la nube
    app.run(host='0.0.0.0', port=port)