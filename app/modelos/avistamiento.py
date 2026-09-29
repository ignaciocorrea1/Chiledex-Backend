from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class AvistamientoModel(BaseModel):
    id: UUID
    id_usuario: int
    especie_id: int
    fecha: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    fotografia_url: Optional[str] = None
    con_geolocalizacion: bool