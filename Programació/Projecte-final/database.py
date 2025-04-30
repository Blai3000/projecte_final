import mysql.connector

# Obrim connexió a la base de dades
def connectar_bbdd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port = "3306",	
        # password="contrasenya",
        database="gestor_tasques"
    )

    cursor = conn.cursor()

    return [conn, cursor]

# Tancar connexió amb la base de dades
def tancar_connexio_bbdd(conn, cursor):
    cursor.close()
    conn.close()