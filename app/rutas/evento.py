from fastapi import APIRouter
from app.modelos.evento import EventoModel
from typing import List
import app.servicios.evento_servicio as svc

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("/", response_model=List[EventoModel])
def eventos_activos():
    return svc.obtener_eventos_activos()