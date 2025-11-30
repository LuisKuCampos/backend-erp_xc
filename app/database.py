import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
# --- CORRECCIÓN AQUÍ: Importamos AsyncSession desde sqlmodel, no sqlalchemy ---
from sqlmodel.ext.asyncio.session import AsyncSession

# 1. Obtener URL
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# 2. Corrección para NEON
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# 3. MOTOR ASÍNCRONO
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# 4. MOTOR SÍNCRONO (Para crear tablas)
SYNC_DATABASE_URL = DATABASE_URL
if "+aiosqlite" in SYNC_DATABASE_URL:
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("+aiosqlite", "")
if "+asyncpg" in SYNC_DATABASE_URL:
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("+asyncpg", "")

sync_engine = create_engine(SYNC_DATABASE_URL)

# 5. Configuración de sesión
# Usamos la AsyncSession que importamos de SQLModel
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

def create_db_and_tables():
    SQLModel.metadata.create_all(sync_engine)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session