from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery

from db import get_or_create_user, update_language, get_session, User
from localization import t
from keyboards.menus import main_menu_kb, language_kb, text_models_kb, image_models_kb

router = Router(name="menu")


@router.callback_query(F.data == "menu:main")
async def on_main_menu(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id)
    lang = user.language
    await callback.message.edit_text(t(lang, "menu_main"), reply_markup=main_menu_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "menu:language")
async def on_language_menu(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id)
    lang = user.language
    await callback.message.edit_text(t(lang, "choose_language"), reply_markup=language_kb(lang))
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def on_set_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    update_language(callback.from_user.id, lang)
    user = get_or_create_user(callback.from_user.id)
    await callback.message.edit_text(t(lang, "menu_main"), reply_markup=main_menu_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "menu:text_ai")
async def on_text_ai_menu(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id)
    lang = user.language
    await callback.message.edit_text(t(lang, "text_ai_choose_model"), reply_markup=text_models_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "menu:image_ai")
async def on_image_ai_menu(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id)
    lang = user.language
    await callback.message.edit_text(t(lang, "image_ai_choose_model"), reply_markup=image_models_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "menu:profile")
async def on_profile(callback: CallbackQuery):
    db = get_session()
    try:
        user: User | None = db.query(User).filter(User.id == callback.from_user.id).first()
    finally:
        db.close()

    if not user:
        user = get_or_create_user(callback.from_user.id)

    lang = user.language
    until_str = user.subscription_until.strftime("%Y-%m-%d %H:%M") if user.subscription_until else "-"

    text = t(
        lang,
        "profile_info",
        user_id=user.id,
        lang=user.language,
        text_model=user.text_model,
        image_model=user.image_model,
        sub=user.subscription,
        until=until_str,
    )
    await callback.message.edit_text(text, reply_markup=main_menu_kb(lang))
    await callback.answer()
