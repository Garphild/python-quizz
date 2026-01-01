from contextlib import asynccontextmanager

from providers.postgree_provider import make_engine, make_sessionmaker, Base

@asynccontextmanager
async def lifespan(app):
    db_engine = make_engine()
    app.state.db_engine = db_engine
    app.state.db_sessionmaker = make_sessionmaker(db_engine)

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        await db_engine.dispose()