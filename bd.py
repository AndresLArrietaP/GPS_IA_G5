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
                LONGITUD FLOAT,
                FECHA_HORA TIMESTAMP DEFAULT CURRENT_TIMESTAMP          
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

    cursor.execute("""SELECT 
                   ID, UBICACION, LATITUD, LONGITUD, strftime('%H:%M:%S', FECHA_HORA) AS HORA 
                   FROM ASISTENCIAS;""")

    return cursor.fetchall()

def eliminarviejo():
    con = conexion.connect('Data.sql')

    cursor = con.cursor()

    cursor.execute("""
        DELETE FROM ASISTENCIAS
        WHERE CAST(FECHA_HORA AS DATE) <> CAST(CURRENT_TIMESTAMP AS DATE)

    """)

    con.commit()
    con.close()