from pydantic import BaseModel
from typing import Optional, List

class FotografiaModel(BaseModel):
    id: int
    url: str
    orden: int

class EspecieModel(BaseModel):
    id: int
    nombre_comun: str
    nombre_cientifico: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: str
    estado_conservacion: Optional[str] = None
    tamanio: Optional[str] = None
    peso: Optional[str] = None
    fotografias: List[FotografiaModel] = []

class RegionModel(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None