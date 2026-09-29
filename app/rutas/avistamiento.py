from fastapi import APIRouter, Query
from typing import Optional
import app.servicios.avistamiento_servicio as svc

router = APIRouter(prefix="/avistamientos", tags=["Avistamientos"])

@router.get("/mapa")
def mapa():
    """Todos los avistamientos con coordenadas."""
    return svc.obtener_avistamientos_mapa()

@router.get("/zona")
def zona(
    lat_min: float = Query(...),
    lat_max: float = Query(...),
    lon_min: float = Query(...),
    lon_max: float = Query(...),
):
    """Avistamientos dentro del área visible del mapa."""
    return svc.obtener_avistamientos_en_zona(lat_min, lat_max, lon_min, lon_max)