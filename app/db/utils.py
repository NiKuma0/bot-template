from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.future import select

from .models import User, Base


async def get_or_create_user(session: AsyncSession, tg_user: TgUser) -> User:
    query_result = await session.execute(
        select(User).where(User.id == tg_user.id)
    )
    user = query_result.scalars().first()

    if not user:
        user = User(
            id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
        )
        session.add(user)
        await session.commit()
    return user


async def create_tables(engine: AsyncEngine, drop_all: bool = False) -> None:
    async with engine.begin() as conn:
        if drop_all:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
