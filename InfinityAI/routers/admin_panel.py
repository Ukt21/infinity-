from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_IDS
from db import get_or_create_user, set_subscription
from localization import t

router = Router(name="admin_panel")


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        user = get_or_create_user(message.from_user.id)
        lang = user.language
        await message.answer(t(lang, "not_admin"))
        return

    user = get_or_create_user(message.from_user.id)
    lang = user.language
    await message.answer(t(lang, "admin_panel"))


@router.message(Command("give_sub"))
async def cmd_give_sub(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        user = get_or_create_user(message.from_user.id)
        lang = user.language
        await message.answer(t(lang, "not_admin"))
        return

    parts = message.text.split()
    if len(parts) < 4:
        await message.answer("Формат: /give_sub user_id tier days\nНапример: /give_sub 123456789 premium 30")
        return

    try:
        target_id = int(parts[1])
        tier = parts[2]
        days = int(parts[3])
    except ValueError:
        await message.answer("Неверные аргументы. Пример: /give_sub 123456789 premium 30")
        return

    if tier not in ("free", "premium", "pro"):
        await message.answer("Тариф должен быть: free / premium / pro")
        return

    set_subscription(target_id, tier, days)
    await message.answer(f"Подписка {tier} на {days} дней выдана пользователю {target_id}.")
