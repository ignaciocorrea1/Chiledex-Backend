from fastapi import APIRouter
from app.modelos.usuario import LoginRequest, RecuperarRequest, RegistroRequest, EditarPerfilRequest, RestablecerRequest, UsuarioResponse
from app.servicios import usuario_servicio as svc

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/login")
def login(body: LoginRequest):
    return svc.login(body.correo, body.contrasena)

@router.post("/registro", status_code=201)
def registro(body: RegistroRequest):
    return svc.registrar(body)

@router.post("/recuperar")
def recuperar(body: RecuperarRequest):
    return svc.buscar_correo(body.correo)

@router.post("/restablecer")
def restablecer(body: RestablecerRequest):
    return svc.restablecer_contrasena(body.correo, body.nueva_contrasena)

@router.put("/{id_usuario}")
def editar_perfil(id_usuario: int, body: EditarPerfilRequest):
    return svc.editar_perfil(id_usuario, body)

@router.get("/{usuario_id}/perfil", response_model=UsuarioResponse)
def obtener_perfil(usuario_id: int):
    return svc.obtener_perfil(usuario_id)