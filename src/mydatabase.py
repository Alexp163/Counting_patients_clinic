from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from database import engine
from models import Base


async def init_app() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn, checkfirst=True))

if __name__ == '__main__':
    import asyncio
    asyncio.run(init_app())

# # Создаём таблицу в базе данных  
# metadata = Base.metadata
# metadata.create_all(engine)  


