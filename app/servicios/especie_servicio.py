from fastapi import HTTPException
from app.base_datos.conexion import get_client
from typing import Optional

CATEGORIAS_VALIDAS = {"FLORA","MAMIFERO","AVE","REPTIL","ANFIBIO","INSECTO"}

def obtener_especies_destacadas(ids: list[int]) -> list[dict]:
    db = get_client()

    # Obtener las especies por los ids indicados
    res = db.table("especie").select("*").in_("id", ids).execute()
    especies = res.data

    if not especies:
        raise HTTPException(status_code=404, detail="No se encontraron especies")

    # Para cada especie, obtener sus fotografías ordenadas
    for especie in especies:
        fotos = (
            db.table("especie_fotografia")
            .select("*")
            .eq("especie_id", especie["id"])
            .order("orden")
            .execute()
        )
        especie["fotografias"] = fotos.data

    return especies


def obtener_regiones() -> list[dict]:
    db = get_client()
    # res = db.table("region").select("*").order("id").execute()
    res = db.table("region").select("*").in_("id", [14, 16]).order("id").execute()
    return res.data

def obtener_catalogo(
    categoria: str | None = None,
    estado_conservacion: list[str] | None = None,
    habitat_ids: list[int] | None = None,
    region_ids: list[int] | None = None,
    busqueda: str | None = None,
    orden: str = "asc",
) -> list[dict]:
    db = get_client()

    query = db.table("especie").select(
        "*, especie_fotografia(id, url, orden)"
    )

    # Filtro por categoría
    if categoria:
        query = query.eq("categoria", categoria.upper())

    # Filtro por estado de conservación (múltiples valores)
    if estado_conservacion:
        query = query.in_("estado_conservacion", estado_conservacion)

    # Filtro por búsqueda de texto
    if busqueda:
        query = query.ilike("nombre_comun", f"%{busqueda}%")

    # Ordenar por nombre común
    query = query.order("nombre_comun", desc=(orden == "desc"))

    res = query.execute()
    especies = res.data

    # Filtro por hábitat (post-query porque requiere join)
    if habitat_ids:
        ids_habitats = set(habitat_ids)
        filtradas = []
        for especie in especies:
            rel = db.table("habitat_especie") \
                    .select("id_habitat") \
                    .eq("id_especie", especie["id"]) \
                    .in_("id_habitat", list(ids_habitats)) \
                    .execute()
            if rel.data:
                filtradas.append(especie)
        especies = filtradas

    # Filtro por región (post-query: region → habitat → especie)
    if region_ids:
        ids_regiones = set(region_ids)
        filtradas = []
        for especie in especies:
            # Hábitats de la especie
            habitats = db.table("habitat_especie") \
                         .select("id_habitat") \
                         .eq("id_especie", especie["id"]) \
                         .execute()
            ids_hab = [h["id_habitat"] for h in habitats.data]
            if not ids_hab:
                continue
            # Regiones de esos hábitats
            regiones = db.table("habitat_region") \
                         .select("id_region") \
                         .in_("id_habitat", ids_hab) \
                         .in_("id_region", list(ids_regiones)) \
                         .execute()
            if regiones.data:
                filtradas.append(especie)
        especies = filtradas

    # Adjuntar primer hábitat como texto para la card
    for especie in especies:
        hab = db.table("habitat_especie") \
                .select("habitat(nombre)") \
                .eq("id_especie", especie["id"]) \
                .limit(1) \
                .execute()
        especie["habitat_nombre"] = (
            hab.data[0]["habitat"]["nombre"] if hab.data else None
        )

    return especies


def obtener_habitats() -> list[dict]:
    db = get_client()
    return db.table("habitat").select("id, nombre").order("nombre").execute().data


def obtener_conteo_por_estado() -> list[dict]:
    """Devuelve cuántas especies hay por estado de conservación."""
    db = get_client()
    res = db.table("especie").select("estado_conservacion").execute()
    conteos: dict[str, int] = {}
    for e in res.data:
        estado = e["estado_conservacion"] or "Sin clasificar"
        conteos[estado] = conteos.get(estado, 0) + 1
    return [{"estado": k, "cantidad": v} for k, v in conteos.items()]

def obtener_detalle_especie(id_especie: int, id_usuario: int | None = None) -> dict:
    """
    Devuelve la ficha completa de una especie:
    - Datos básicos + fotografías
    - Hábitats asociados
    - Avistamientos del usuario para esa especie (si se pasa id_usuario)
    """
    db = get_client()

    # ── Especie base ──────────────────────────────────────────────────────
    res = db.table("especie").select("*").eq("id", id_especie).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    especie = res.data

    # ── Fotografías ordenadas ─────────────────────────────────────────────
    fotos = db.table("especie_fotografia") \
              .select("*") \
              .eq("especie_id", id_especie) \
              .order("orden") \
              .execute()
    especie["fotografias"] = fotos.data

    # ── Hábitats asociados ────────────────────────────────────────────────
    habitats = db.table("habitat_especie") \
                 .select("habitat(id, nombre, descripcion)") \
                 .eq("id_especie", id_especie) \
                 .execute()
    especie["habitats"] = [h["habitat"] for h in habitats.data]

    # ── Avistamientos del usuario para esta especie ───────────────────────
    if id_usuario:
        avist = db.table("avistamiento") \
                  .select("id, fecha, lugar:latitud, longitud, fotografia_url") \
                  .eq("especie_id", id_especie) \
                  .eq("id_usuario", id_usuario) \
                  .order("fecha", desc=True) \
                  .execute()
        especie["mis_avistamientos"] = avist.data
    else:
        especie["mis_avistamientos"] = []

    return especie