import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.settings import get_settings
from app.db.middlewares import DbMiddleware, AutoUserCreate
from app.db.utils import create_tables
from app.handlers.main import main_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_bot():
    settings = get_settings()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    logger.info('Connecting to "%s"', settings.postgres_dsn, exc_info=1)
    engine = create_async_engine(settings.postgres_dsn, echo=True)
    session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    await create_tables(engine, drop_all=True)

    dp.update.middleware(DbMiddleware(session_maker))
    dp.update.middleware(AutoUserCreate())
    dp.include_router(main_router)

    await dp.start_polling(bot, settings=settings)
