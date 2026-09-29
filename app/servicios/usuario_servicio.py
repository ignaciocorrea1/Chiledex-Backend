from passlib.context import CryptContext
from fastapi import HTTPException
from app.base_datos.conexion import get_client
from app.modelos.usuario import RegistroRequest, EditarPerfilRequest

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def login(correo: str, contrasena: str) -> dict:
    db = get_client()
    res = db.table("usuario").select("*").eq("correo", correo).single().execute()
    usuario = res.data
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # ── Comparación temporal en texto plano (sin hash) ──
    if contrasena != usuario["contrasena_hash"]:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    db.table("usuario").update({"logeado": True}).eq("id", usuario["id"]).execute()
    return {k: v for k, v in usuario.items() if k != "contrasena_hash"}

def registrar(data: RegistroRequest) -> dict:
    db = get_client()
    
    existente = db.table("usuario").select("id").eq("correo", data.correo).execute()
    if existente.data:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    nuevo = {
        "correo":          data.correo,
        "contrasena_hash": data.contrasena,  # ← sin hash por ahora
        "nombre":          data.nombre,
        "ap_paterno":      data.ap_paterno,
        "ap_materno":      data.ap_materno,
    }
    
    res = db.table("usuario").insert(nuevo).execute()
    usuario = res.data[0]
    return {k: v for k, v in usuario.items() if k != "contrasena_hash"}

def buscar_correo(correo: str) -> dict:
    db = get_client()
    res = db.table("usuario").select("id", "correo").eq("correo", correo).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="No encontramos una cuenta con ese correo")
    return {"encontrado": True, "correo": correo}

def restablecer_contrasena(correo: str, nueva_contrasena: str) -> dict:
    db = get_client()
    # Verificar que el correo existe
    res = db.table("usuario").select("id").eq("correo", correo).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Correo no encontrado")
    
    # Actualizar la contraseña directamente (sin hash por ahora)
    db.table("usuario").update(
        {"contrasena_hash": nueva_contrasena}
    ).eq("correo", correo).execute()
    
    return {"mensaje": "Contraseña restablecida correctamente"}

def editar_perfil(id_usuario: int, data: EditarPerfilRequest) -> dict:
    db = get_client()

    # Construir solo los campos que vienen con valor
    campos = {k: v for k, v in data.model_dump().items() if v is not None}

    if not campos:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    # Verificar correo duplicado si se está cambiando
    if "correo" in campos:
        existente = db.table("usuario") \
                      .select("id") \
                      .eq("correo", campos["correo"]) \
                      .neq("id", id_usuario) \
                      .execute()
        if existente.data:
            raise HTTPException(status_code=400, detail="El correo ya está en uso")

    res = db.table("usuario") \
            .update(campos) \
            .eq("id", id_usuario) \
            .execute()

    if not res.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario = res.data[0]
    return {k: v for k, v in usuario.items() if k != "contrasena_hash"}

def obtener_perfil(usuario_id: int) -> dict:
    db = get_client()
    res = db.table("usuario").select(
        "id, correo, nombre, ap_paterno, ap_materno, foto_perfil_url, racha_actual, created_at"
    ).eq("id", usuario_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return res.data

