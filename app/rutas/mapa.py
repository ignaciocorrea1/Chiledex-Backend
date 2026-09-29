from fastapi import APIRouter
from app.servicios import mapa_servicio as svc

router = APIRouter(prefix="/mapa", tags=["Mapa"])

@router.get("/avistamientos")
def avistamientos():
    return svc.listar_avistamientos()