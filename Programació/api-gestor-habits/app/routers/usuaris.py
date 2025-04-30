from fastapi import APIRouter
from pydantic import BaseModel
import database

router = APIRouter(tags=["usuaris"])

# Entitat tasques

class Usuari(BaseModel):
    id: int
    nom: str
    llinatges: str
    email: str
    contrassenya: str

def user_to_string(user_tuple):
    res = { "id": user_tuple[0], 
            "nom": user_tuple[1], 
            "llinatges": user_tuple[2], 
            "email": user_tuple[3], 
            "sexe": user_tuple[4],
            "contra": user_tuple[5],
            "telefon": user_tuple[6],
            "altura": user_tuple[7],
            "pes": user_tuple[8],
            "imc": user_tuple[9] }
    return res

@router.get("/usuaris")
async def usuaris():
    [conn, cursor] = database.connectar_bbdd()
    cursor.execute("SELECT * FROM USUARIS")
    resultats = cursor.fetchall()
    res = { "usuaris": [] }
    for fila in resultats:
        res['usuaris'].append(user_to_string(fila))
    database.tancar_connexio_bbdd(conn, cursor)
    return res

@router.get("/usuaris/{id}")
async def usuari(id: int):
    [conn, cursor] = database.connectar_bbdd()
    print("Hola")
    cursor.execute(f"SELECT * FROM USUARIS WHERE id = {id}")
    resultats = cursor.fetchall()
    res = { "usuaris": [] }
    for fila in resultats:
        res['usuaris'].append(user_to_string(fila))
    database.tancar_connexio_bbdd(conn, cursor)
    return res

@router.post("/usuari")
async def afegir_usuari(usuari: Usuari):
    pass

@router.put("/usuari")
async def modificar_usuari(usuari: Usuari):
    pass

@router.delete("/usuari/{id}")
async def eliminar_usuari(id: int):
    pass