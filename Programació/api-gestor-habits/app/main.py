from fastapi import FastAPI
from routers import tasques, usuaris
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(tasques.router)
app.include_router(usuaris.router)
# app.mount("/static", StaticFiles(directory="static"), name="static")