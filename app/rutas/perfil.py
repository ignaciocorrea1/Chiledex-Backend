from fastapi import APIRouter
from app.servicios import perfil_servicios as svc

router = APIRouter(prefix="/perfil", tags=["Perfil"])

@router.get("/{id_usuario}")
def perfil(id_usuario: int):
    return svc.obtener_perfil(id_usuario)

@router.get("/{id_usuario}/logros")
def todos_logros(id_usuario: int):
    return svc.obtener_todos_logros(id_usuario)