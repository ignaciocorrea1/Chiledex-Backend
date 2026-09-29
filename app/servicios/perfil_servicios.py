from fastapi import HTTPException
from app.base_datos.conexion import get_client


def obtener_perfil(id_usuario: int) -> dict:
    """
    Devuelve toda la información necesaria para el perfil:
    - Datos del usuario
    - Contadores (especies únicas, avistamientos, logros)
    - Racha actual
    - Últimos logros (máx 4)
    - Últimos avistamientos (máx 5)
    """
    db = get_client()

    # ── Datos básicos del usuario ─────────────────────────────────────────
    res = db.table("usuario") \
            .select("id, nombre, ap_paterno, foto_perfil_url, racha_actual, created_at") \
            .eq("id", id_usuario) \
            .single() \
            .execute()

    if not res.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario = res.data

    # ── Conteo de avistamientos totales ───────────────────────────────────
    avist = db.table("avistamiento") \
              .select("id", count="exact") \
              .eq("id_usuario", id_usuario) \
              .execute()
    total_avistamientos = avist.count or 0

    # ── Conteo de especies únicas avistadas ───────────────────────────────
    especies = db.table("avistamiento") \
                 .select("especie_id") \
                 .eq("id_usuario", id_usuario) \
                 .execute()
    total_especies = len({a["especie_id"] for a in especies.data})

    # ── Logros del usuario (máx 4 para insignias) ─────────────────────────
    logros_res = db.table("usuario_logro") \
                   .select("fecha_obtencion, logro(id, nombre, descripcion, icono)") \
                   .eq("id_usuario", id_usuario) \
                   .order("fecha_obtencion", desc=True) \
                   .limit(4) \
                   .execute()
    logros = [
        {
            "id":              l["logro"]["id"],
            "nombre":          l["logro"]["nombre"],
            "descripcion":     l["logro"]["descripcion"],
            "icono":           l["logro"]["icono"],
            "fecha_obtencion": l["fecha_obtencion"],
        }
        for l in logros_res.data
    ]
    total_logros = db.table("usuario_logro") \
                     .select("id_logro", count="exact") \
                     .eq("id_usuario", id_usuario) \
                     .execute().count or 0

    # ── Últimos avistamientos con especie y foto ───────────────────────────
    ultimos_res = db.table("avistamiento") \
                    .select("""
                        id, fecha, fotografia_url,
                        especie:especie_id (
                            id, nombre_comun,
                            especie_fotografia (url, orden)
                        )
                    """) \
                    .eq("id_usuario", id_usuario) \
                    .order("fecha", desc=True) \
                    .limit(5) \
                    .execute()

    ultimos = []
    for a in ultimos_res.data:
        fotos = a.get("especie", {}).get("especie_fotografia", [])
        fotos_ord = sorted(fotos, key=lambda f: f["orden"])
        ultimos.append({
            "id":           a["id"],
            "fecha":        a["fecha"],
            "foto_url":     fotos_ord[0]["url"] if fotos_ord else None,
            "especie_id":   a["especie"]["id"],
            "especie_nombre": a["especie"]["nombre_comun"],
        })

    return {
        "usuario":            usuario,
        "total_especies":     total_especies,
        "total_avistamientos": total_avistamientos,
        "total_logros":       total_logros,
        "logros":             logros,
        "ultimos_avistamientos": ultimos,
    }
    
def obtener_todos_logros(id_usuario: int) -> list[dict]:
    """
    Devuelve TODOS los logros del sistema, marcando cuáles
    tiene el usuario y cuáles están bloqueados.
    Los logros sorpresa bloqueados ocultan nombre e ícono.
    """
    db = get_client()

    # Todos los logros del sistema
    todos = db.table("logro").select("*").order("id").execute().data

    # Logros que el usuario ya obtuvo
    obtenidos_res = db.table("usuario_logro") \
                      .select("id_logro, fecha_obtencion") \
                      .eq("id_usuario", id_usuario) \
                      .execute()

    # Mapa rápido: id_logro → fecha_obtencion
    obtenidos = {
        r["id_logro"]: r["fecha_obtencion"]
        for r in obtenidos_res.data
    }

    resultado = []
    for logro in todos:
        obtenido      = logro["id"] in obtenidos
        es_sorpresa   = logro["es_sorpresa"]
        fecha         = obtenidos.get(logro["id"])

        resultado.append({
            "id":             logro["id"],
            # Si es sorpresa y no está obtenido, ocultar nombre e ícono
            "nombre":  logro["nombre"] if (obtenido or not es_sorpresa) else "???",
            "icono":   logro["icono"]  if (obtenido or not es_sorpresa) else "",
            "descripcion": logro["descripcion"] if obtenido else None,
            "obtenido":       obtenido,
            "fecha_obtencion": fecha,
        })

    return resultado