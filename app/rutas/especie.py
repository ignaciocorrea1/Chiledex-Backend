from fastapi import APIRouter, Query
from typing import Optional
from app.servicios import especie_servicio as svc

router = APIRouter(prefix="/especies", tags=["Especies"])

@router.get("/destacadas")
def destacadas():
    # Momentáneo: solo ids 1, 2, 3
    return svc.obtener_especies_destacadas([1, 2, 3])

@router.get("/regiones")
def regiones():
    return svc.obtener_regiones()

@router.get("/catalogo")
def catalogo(
    categoria:           Optional[str]       = Query(None),
    estado_conservacion: Optional[list[str]] = Query(None),
    habitat_ids:         Optional[list[int]] = Query(None),
    region_ids:          Optional[list[int]] = Query(None),
    busqueda:            Optional[str]        = Query(None),
    orden:               str                  = Query("asc"),
):
    return svc.obtener_catalogo(
        categoria, estado_conservacion,
        habitat_ids, region_ids, busqueda, orden,
    )

@router.get("/habitats")
def habitats():
    return svc.obtener_habitats()

@router.get("/conteo-estados")
def conteo_estados():
    return svc.obtener_conteo_por_estado()

@router.get("/{id_especie}")
def detalle_especie(
    id_especie: int,
    id_usuario: Optional[int] = Query(None),
):
    return svc.obtener_detalle_especie(id_especie, id_usuario)