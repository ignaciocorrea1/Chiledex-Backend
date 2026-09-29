from fastapi import HTTPException
from app.base_datos.conexion import get_client


def obtener_avistamientos_mapa() -> list[dict]:
    """
    Devuelve todos los avistamientos que tienen coordenadas,
    con información básica de la especie para el marker y la card.
    """
    db = get_client()

    res = db.table("avistamiento") \
            .select("""
                id, fecha, latitud, longitud, fotografia_url,
                especie:especie_id (
                    id, nombre_comun, categoria,
                    especie_fotografia (url, orden)
                )
            """) \
            .eq("con_geolocalizacion", True) \
            .not_.is_("latitud", "null") \
            .not_.is_("longitud", "null") \
            .order("fecha", desc=True) \
            .execute()

    avistamientos = res.data

    # Ordenar fotos y dejar solo la portada
    for a in avistamientos:
        fotos = a.get("especie", {}).get("especie_fotografia", [])
        fotos_ord = sorted(fotos, key=lambda f: f["orden"])
        a["especie"]["foto_portada"] = fotos_ord[0]["url"] if fotos_ord else None
        del a["especie"]["especie_fotografia"]

    return avistamientos


def obtener_avistamientos_en_zona(
    lat_min: float, lat_max: float,
    lon_min: float, lon_max: float,
) -> list[dict]:
    """
    Filtra avistamientos dentro de un bounding box (área visible del mapa).
    """
    db = get_client()

    res = db.table("avistamiento") \
            .select("""
                id, fecha, latitud, longitud, fotografia_url,
                especie:especie_id (
                    id, nombre_comun, categoria,
                    especie_fotografia (url, orden)
                )
            """) \
            .eq("con_geolocalizacion", True) \
            .gte("latitud",  lat_min).lte("latitud",  lat_max) \
            .gte("longitud", lon_min).lte("longitud", lon_max) \
            .order("fecha", desc=True) \
            .execute()

    avistamientos = res.data

    for a in avistamientos:
        fotos = a.get("especie", {}).get("especie_fotografia", [])
        fotos_ord = sorted(fotos, key=lambda f: f["orden"])
        a["especie"]["foto_portada"] = fotos_ord[0]["url"] if fotos_ord else None
        del a["especie"]["especie_fotografia"]

    return avistamientos