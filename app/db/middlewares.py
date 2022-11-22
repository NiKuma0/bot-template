from aiogram.dispatcher.middlewares.base import BaseMiddleware

from .utils import get_or_create_user


class DbMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker) -> None:
        self.session_maker = sessionmaker

    async def __call__(self, handler, event, data):
        async with self.session_maker() as session:
            data["session"] = session
            return await handler(event, data)


class AutoUserCreate(BaseMiddleware):
    async def __call__(self, handler, event, data):
        assert (session := data.get("session", False))

        data["user"] = None
        if tg_user := data.get("event_from_user"):
            data["user"] = await get_or_create_user(session, tg_user)
        return await handler(event, data)
