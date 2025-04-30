from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["tasques"])

# Entitat tasques

class Tasca(BaseModel):
    id: int
    titol: str
    descripcio: str
    estat: str
    data: str

@router.get("/tasques")
async def tasques():
    pass

@router.get("/tasques/{id}")
async def tasca(id: int):
    pass

@router.post("/tasca/", response_model=Tasca, status_code=201)
async def afegir_tasca(tasca: Tasca):
    pass

@router.put("/tasca")
async def modificar_tasca(tasca: Tasca):
    pass

@router.delete("/tasca/{id}")
async def eliminar_tasca(id: int):
    pass