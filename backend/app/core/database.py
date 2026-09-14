from collections.abc import AsyncGenerator
import logging
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


logger = logging.getLogger(__name__)

encoded_password = quote_plus(settings.db_password)

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{encoded_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)

logger.info(
    "Connecting to database: %s on %s:%s",
    settings.db_name,
    settings.db_host,
    settings.db_port,
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()