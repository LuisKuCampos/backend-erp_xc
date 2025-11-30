from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables, get_session
from .deps import verify_api_key, parse_filter_query
from .models import SerieDocumentos, Usuario, Entidad, Articulo, Cotizacion, CotizacionLinea
from .schemas import ArticuloCreate, ArticuloUpdate, CotizacionCreate, CotizacionUpdate
from .crud import get_all_paginated, create_generic, update_generic, delete_generic
from .seed import run_seed
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables() # Tablas
    asyncio.create_task(run_seed()) # Datos prueba

# Helper para respuesta JSON consistente
def format_resp(key: str, data, total):
    # Convertimos objetos SQLModel a dict
    return {"count": len(data), "total_count": total, key: data}

# --- ENDPOINTS ---

@app.get("/art_ma", dependencies=[Depends(verify_api_key)])
async def get_articulos(req: Request, page: int = 1, limit: int = 20, session=Depends(get_session)):
    filters = parse_filter_query(req)
    items, total = await get_all_paginated(session, Articulo, page, limit, filters)
    return format_resp("art_ma", items, total)

@app.post("/art_ma", dependencies=[Depends(verify_api_key)])
async def create_articulo(item: ArticuloCreate, session=Depends(get_session)):
    new_art = Articulo.from_orm(item)
    return await create_generic(session, new_art)

@app.put("/art_ma/{id}", dependencies=[Depends(verify_api_key)])
async def update_articulo(id: int, item: ArticuloUpdate, session=Depends(get_session)):
    res = await update_generic(session, Articulo, id, item.dict(exclude_unset=True))
    if not res: raise HTTPException(404, "No encontrado")
    return res

@app.delete("/art_ma/{id}", dependencies=[Depends(verify_api_key)])
async def delete_articulo(id: int, session=Depends(get_session)):
    res = await delete_generic(session, Articulo, id)
    if not res: raise HTTPException(404, "No encontrado")
    return {"ok": True}

# --- COTIZACIONES (Transaccional) ---

@app.get("/vta_pre_gv", dependencies=[Depends(verify_api_key)])
async def get_cotizaciones(req: Request, page: int = 1, limit: int = 20, session=Depends(get_session)):
    filters = parse_filter_query(req)
    items, total = await get_all_paginated(session, Cotizacion, page, limit, filters)
    return format_resp("vta_pre_gv", items, total)

@app.post("/vta_pre_gv", dependencies=[Depends(verify_api_key)])
async def create_cotizacion(item: CotizacionCreate, session=Depends(get_session)):
    # Aquí podrías agregar lógica para generar el ser_fol automáticamente
    new_cot = Cotizacion.from_orm(item)
    new_cot.ser_fol = "NUEVO-001" 
    return await create_generic(session, new_cot)

@app.get("/vta_pre_lin", dependencies=[Depends(verify_api_key)])
async def get_lineas(req: Request, cot_id: int, session=Depends(get_session)):
    # Filtro manual porque este endpoint lo pide específico
    items, total = await get_all_paginated(session, CotizacionLinea, 1, 100, {"cot_id": cot_id})
    return format_resp("vta_pre_lin", items, total)

# --- OTROS CATALOGOS (Solo lectura por brevedad, agrega POST si quieres) ---

@app.get("/ser_doc_cfg", dependencies=[Depends(verify_api_key)])
async def get_series(req: Request, session=Depends(get_session)):
    items, total = await get_all_paginated(session, SerieDocumentos, 1, 100, {})
    return format_resp("ser_doc_cfg", items, total)

@app.get("/usr_vb", dependencies=[Depends(verify_api_key)])
async def get_users(req: Request, session=Depends(get_session)):
    items, total = await get_all_paginated(session, Usuario, 1, 100, {})
    return format_resp("usr_vb", items, total)

@app.get("/ent_ma", dependencies=[Depends(verify_api_key)])
async def get_ents(req: Request, session=Depends(get_session)):
    items, total = await get_all_paginated(session, Entidad, 1, 100, {})
    return format_resp("ent_ma", items, total)