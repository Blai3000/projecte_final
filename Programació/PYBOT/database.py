import mysql.connector

def obrir_connexio():
    # Connexió a la base de dades
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port = "3307",
        # password="contrasenya",
        database="gestor_tasques"
    )

    cursor = conn.cursor()
    return [conn, cursor]

# Executar una consulta SQL
# cursor.execute("SELECT * FROM clients")

# # Obtenir els resultats
# resultats = cursor.fetchall()
# for fila in resultats:
#     print(fila)

def tancar_connexio(conn, cursor):
    # Tancar la connexió
    cursor.close()
    conn.close()
