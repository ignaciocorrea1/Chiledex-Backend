from fastapi import FastAPI
from app.rutas import especie, mapa, usuario, avistamiento, perfil, evento
from fastapi.middleware.cors import CORSMiddleware

APP_TITLE = "ChileDex API"
ALLOWED_ORIGINS = ["*"]

app = FastAPI(title=APP_TITLE, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(especie.router)

@app.get("/")
def root():
    return {"status": "ChileDex API online"}

app.include_router(usuario.router)
app.include_router(especie.router)
app.include_router(mapa.router)
app.include_router(avistamiento.router)
app.include_router(perfil.router)
app.include_router(evento.router)