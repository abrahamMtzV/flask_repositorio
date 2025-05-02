import sqlite3

conn = sqlite3.connect('avisos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS avisos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Base de datos y tabla creada.")