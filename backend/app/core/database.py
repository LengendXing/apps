from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=settings.ENVIRONMENT == "development")
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        from app.models.base import Base
        # Import all models so they are registered with Base.metadata
        import app.models.user  # noqa: F401
        import app.models.category  # noqa: F401
        import app.models.tool  # noqa: F401
        import app.models.file_upload  # noqa: F401
        import app.models.audit_log  # noqa: F401
        import app.models.setting  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)
    # Seed default data
    from sqlalchemy import select
    from app.models.setting import Setting
    from app.models.user import User
    from app.core.security import hash_password
    default_access_password = "Apps2026!"
    default_admin_password = "Admin@123"
    async with async_session() as session:
        existing = await session.execute(select(Setting).where(Setting.key == "access_password"))
        if not existing.scalar_one_or_none():
            session.add(Setting(key="access_password", value=hash_password(default_access_password), description="C端访问密码"))
            await session.commit()
        existing_user = await session.execute(select(User).where(User.username == "admin"))
        if not existing_user.scalar_one_or_none():
            session.add(User(username="admin", email="admin@apps.local", password_hash=hash_password(default_admin_password), is_active=True))
            await session.commit()
