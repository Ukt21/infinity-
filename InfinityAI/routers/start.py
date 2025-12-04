from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db import get_or_create_user
from localization import t
from keyboards.menu import main_menu_kb

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = user.language

    text = f"{t(lang, 'start_title')}\n\n{t(lang, 'start_desc')}"
    await message.answer(text, reply_markup=main_menu_kb(lang))

