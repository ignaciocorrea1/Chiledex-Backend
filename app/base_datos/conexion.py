from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Libería para cargar variables de entorno
load_dotenv()

# Variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Creación de instancia del cliente de Supabase
def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)