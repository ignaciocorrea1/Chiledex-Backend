from app.base_datos.conexion import get_client

def listar_avistamientos() -> list:
    db = get_client()
    # Solo avistamientos con coordenadas
    res = db.table("avistamiento").select(
        "id, especie_id, latitud, longitud, fotografia_url, fecha,"
        " especie(nombre_comun)"
    ).not_.is_("latitud", "null").not_.is_("longitud", "null").execute()

    return [
        {
            "id": a["id"],
            "especie_id": a["especie_id"],
            "nombre_comun": a["especie"]["nombre_comun"],
            "latitud": float(a["latitud"]),
            "longitud": float(a["longitud"]),
            "fotografia_url": a["fotografia_url"],
            "fecha": a["fecha"],
        }
        for a in res.data
    ]