from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery

from db import get_session, User
from localization import t
from keyboards.menus import main_menu_kb

router = Router(name="subscription")


@router.callback_query(F.data == "menu:subscription")
async def on_subscription_menu(callback: CallbackQuery):
    db = get_session()
    try:
        user: User | None = db.query(User).filter(User.id == callback.from_user.id).first()
    finally:
        db.close()

    if not user:
        from db import get_or_create_user
        user = get_or_create_user(callback.from_user.id)

    lang = user.language

    if user.subscription != "free" and user.subscription_until:
        until_str = user.subscription_until.strftime("%Y-%m-%d %H:%M")
        text = t(lang, "subscription_info", tier=user.subscription, until=until_str)
    else:
        text = t(lang, "no_subscription")

    extra = "\n\n" + (
        "Оплата через Telegram Stars будет добавлена позже.\n"
        "Сейчас вы можете оплатить на карту и отправить чек админу — он включит подписку вручную."
        if lang == "ru"
        else "Telegram Stars orqali to‘lov keyinroq qo‘shiladi.\n"
             "Hozircha kartaga to‘lov qilib, chekni adminga yuborishingiz mumkin — u obunani qo‘lda yoqadi."
    )

    await callback.message.edit_text(text + extra, reply_markup=main_menu_kb(lang))
    await callback.answer()
