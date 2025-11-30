import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# 1. Obtener URL
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# 2. LIMPIEZA DE URL (Corrección SSL y Driver)
# Primero aseguramos el driver asyncpg
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# AHORA: Quitamos el parámetro 'sslmode' de la URL porque asyncpg no lo soporta ahí
if "?sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?sslmode=")[0]
if "&sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("&sslmode=")[0]

# 3. MOTOR ASÍNCRONO
# Pasamos la configuración SSL en 'connect_args' que es la forma correcta
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
    connect_args={"ssl": "require"} if "postgresql" in DATABASE_URL else {}
)

# 4. MOTOR SÍNCRONO (Para crear tablas)
SYNC_DATABASE_URL = DATABASE_URL
if "+aiosqlite" in SYNC_DATABASE_URL:
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("+aiosqlite", "")
if "+asyncpg" in SYNC_DATABASE_URL:
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("+asyncpg", "")

# El motor síncrono (psycopg2) sí acepta sslmode en la URL, pero como se lo quitamos arriba,
# lo pasamos como argumento también para asegurar conexión segura.
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    connect_args={"sslmode": "require"} if "postgresql" in SYNC_DATABASE_URL else {}
)

# 5. Configuración de sesión
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

def create_db_and_tables():
    SQLModel.metadata.create_all(sync_engine)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session