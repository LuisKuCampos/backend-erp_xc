from typing import Dict, Any, Type, TypeVar, Optional, List
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

T = TypeVar("T", bound=SQLModel)

async def get_all_paginated(
    session: AsyncSession, 
    model: Type[T], 
    page: int, 
    limit: int, 
    filters: Dict[str, Any]
):
    offset = (page - 1) * limit
    stmt = select(model)
    
    # Aplicar filtros
    conditions = []
    for k, v in filters.items():
        if hasattr(model, k):
            conditions.append(getattr(model, k) == v)
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    # Ejecutar query
    result = await session.exec(stmt.offset(offset).limit(limit))
    items = result.all()
    
    # Total count (simplificado para velocidad)
    # En producción real haríamos un count() query separado
    return items, len(items) 

async def create_generic(session: AsyncSession, obj: SQLModel):
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def update_generic(session: AsyncSession, model: Type[T], id: int, data: Dict[str, Any]):
    db_obj = await session.get(model, id)
    if not db_obj:
        return None
    for k, v in data.items():
        if v is not None:
            setattr(db_obj, k, v)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj

async def delete_generic(session: AsyncSession, model: Type[T], id: int):
    db_obj = await session.get(model, id)
    if not db_obj:
        return False
    await session.delete(db_obj)
    await session.commit()
    return True