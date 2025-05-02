from flask import Flask, render_template, request, redirect, url_for
from flask import session
import sqlite3

app = Flask(__name__)

def obtener_avisos():
    conn = sqlite3.connect('avisos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM avisos ORDER BY fecha DESC")
    avisos = cursor.fetchall()
    conn.close()
    return avisos
    

@app.route('/')
def index():
    avisos = obtener_avisos()
    return render_template('index.html', avisos=avisos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_aviso():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        conn = sqlite3.connect('avisos.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO avisos (titulo, descripcion, fecha) VALUES (?, ?, ?)", (titulo, descripcion, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('nuevo.html')

app.secret_key = '123'  # cámbiala por algo más seguro en producción

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario == 'admin' and clave == '1234':
            session['usuario'] = usuario
            return redirect(url_for('nuevo_aviso'))
        else:
            return "Credenciales incorrectas", render_template('login.html')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)