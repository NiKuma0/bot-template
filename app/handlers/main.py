from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


main_router = Router()


@main_router.message(CommandStart())
async def echo(m: Message, user: User):
    await m.answer(f"Hello, {user.full_name}!")


@main_router.message(Command("change_first_name"))
async def change_name(
    m: Message, command: CommandObject, session: AsyncSession, user: User
):
    if not command.args:
        return await m.answer(
            'Поле не может быть пустым. Пример /change_first_name Иван'
        )
    user.first_name = command.args
    await session.commit()
    await m.answer(f"Теперь буду называть вас как: {user.full_name}")


@main_router.message(Command("change_last_name"))
async def change_last_name(
    m: Message, command: CommandObject, session: AsyncSession, user: User
):
    if not command.args:
        return await m.answer(
            'Поле не может быть пустым. Пример /change_last_name Иванов'
        )
    user.last_name = command.args
    await session.commit()
    await m.answer(f"Теперь буду называть вас как: {user.full_name}")
