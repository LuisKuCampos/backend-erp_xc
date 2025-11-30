from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class SerieDocumentos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    doc_mod_name: str
    prefix: Optional[str] = None
    current_number: int = 0
    # Relaciones
    cotizaciones: List["Cotizacion"] = Relationship(back_populates="serie")

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: Optional[str] = None
    email: Optional[str] = None
    cotizaciones: List["Cotizacion"] = Relationship(back_populates="usuario")

class Entidad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    rfc: Optional[str] = None
    address: Optional[str] = None
    cotizaciones: List["Cotizacion"] = Relationship(back_populates="entidad")

class Articulo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: Optional[str] = None
    name: str
    unit: Optional[str] = None
    price: float
    lineas: List["CotizacionLinea"] = Relationship(back_populates="articulo")

class Cotizacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ser_fol: Optional[str] = None
    ser_doc: Optional[int] = Field(default=None, foreign_key="seriedocumentos.id")
    alt_usr: Optional[int] = Field(default=None, foreign_key="usuario.id")
    ent_id: Optional[int] = Field(default=None, foreign_key="entidad.id")
    fecha: Optional[datetime] = Field(default_factory=datetime.utcnow)
    est: int = 0

    serie: Optional[SerieDocumentos] = Relationship(back_populates="cotizaciones")
    usuario: Optional[Usuario] = Relationship(back_populates="cotizaciones")
    entidad: Optional[Entidad] = Relationship(back_populates="cotizaciones")
    lineas: List["CotizacionLinea"] = Relationship(back_populates="cotizacion")

class CotizacionLinea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cot_id: Optional[int] = Field(default=None, foreign_key="cotizacion.id")
    art_id: Optional[int] = Field(default=None, foreign_key="articulo.id")
    cantidad: float
    precio: float
    subtotal: float

    cotizacion: Optional[Cotizacion] = Relationship(back_populates="lineas")
    articulo: Optional[Articulo] = Relationship(back_populates="lineas")