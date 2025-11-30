from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# --- CREATE MODELS (Para recibir datos) ---
class ArticuloCreate(BaseModel):
    code: Optional[str] = None
    name: str
    unit: Optional[str] = None
    price: float

class CotizacionCreate(BaseModel):
    ser_doc: int
    alt_usr: int
    ent_id: int
    est: int = 0

class CotizacionLineaCreate(BaseModel):
    cot_id: int
    art_id: int
    cantidad: float
    precio: float
    subtotal: float

# --- UPDATE MODELS (Para editar) ---
class ArticuloUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class CotizacionUpdate(BaseModel):
    est: Optional[int] = None