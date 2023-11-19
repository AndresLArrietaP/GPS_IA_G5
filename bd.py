import sqlite3 as conexion

con = conexion.connect('Data.sql')

cursor = con.cursor()

def creartabla():
    con = conexion.connect('Data.sql')

    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE ASISTENCIAS(
                ID INTEGER PRIMARY KEY autoincrement,
                UBICACION VARCHAR(50),
                LATITUD FLOAT,
                LONGITUD FLOAT           
        )
    """)

    con.commit()
    con.close()

def insertar(datos):
    con = conexion.connect('Data.sql')

    cursor = con.cursor()

    cursor.executemany("INSERT INTO ASISTENCIAS (UBICACION,LATITUD,LONGITUD) VALUES (?,?,?)",datos)

    con.commit()
    con.close()

def seleccionar():
    con = conexion.connect('Data.sql')

    cursor = con.cursor()

    cursor.execute("SELECT * FROM ASISTENCIAS")

    return cursor.fetchall()