import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# 1. Obtener URL
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# 2. Corrección ROBUSTA para NEON y RENDER
# A veces nos dan "postgres://" y a veces "postgresql://"
# El motor asíncrono EXIGE que diga "postgresql+asyncpg://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 3. MOTOR ASÍNCRONO
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# 4. MOTOR SÍNCRONO (Para crear tablas)
# Aquí hacemos lo opuesto: quitamos la parte asíncrona para usar drivers estándar
SYNC_DATABASE_URL = DATABASE_URL
if "+aiosqlite" in SYNC_DATABASE_URL:
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("+aiosqlite", "")
if "+asyncpg" in SYNC_DATABASE_URL:
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("+asyncpg", "")

sync_engine = create_engine(SYNC_DATABASE_URL)

# 5. Configuración de sesión
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

def create_db_and_tables():
    SQLModel.metadata.create_all(sync_engine)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session