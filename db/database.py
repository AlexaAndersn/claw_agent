from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from contextlib import asynccontextmanager
import os
from core.config import settings
from db.models import Base, recreate_database


class Database:
    def __init__(self):
        import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "claw_agent.db")
        
        # Check if database exists and has old schema
        if os.path.exists(db_path):
            # Recreate database for new schema
            try:
                os.remove(db_path)
                print("Old database removed - creating new one")
            except:
                pass
        
        db_url = "sqlite+aiosqlite:///D:/claw-агент/claw_agent.db"
        self.engine = create_async_engine(
            db_url,
            connect_args={"check_same_thread": False, "uri": True},
            poolclass=StaticPool,
            echo=False,
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db = Database()
