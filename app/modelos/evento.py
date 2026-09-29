from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventoModel(BaseModel):
    id: int
    nombre: str
    fecha: datetime
    lugar: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: bool