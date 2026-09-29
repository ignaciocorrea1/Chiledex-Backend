from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class RegistroRequest(BaseModel):
    correo: EmailStr
    contrasena: str
    nombre: str
    ap_paterno: Optional[str] = None
    ap_materno: Optional[str] = None

class EditarPerfilRequest(BaseModel):
    nombre: Optional[str] = None
    ap_paterno: Optional[str] = None
    ap_materno: Optional[str] = None
    foto_perfil_url: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    correo: str
    nombre: str
    ap_paterno: Optional[str]
    ap_materno: Optional[str]
    foto_perfil_url: Optional[str]
    racha_actual: int
    created_at: datetime
    
class RecuperarRequest(BaseModel):
    correo: EmailStr

class RestablecerRequest(BaseModel):
    correo: EmailStr
    nueva_contrasena: str
    