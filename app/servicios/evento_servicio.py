from app.base_datos.conexion import get_client


def obtener_eventos_activos() -> list[dict]:
    """Devuelve los eventos activos ordenados por fecha más próxima."""
    db = get_client()
    res = db.table("evento") \
            .select("*") \
            .eq("activo", True) \
            .order("fecha", desc=False) \
            .execute()
    return res.data