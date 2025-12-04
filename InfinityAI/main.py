import os
import asyncio
import logging
import sqlite3
from datetime import datetime, timedelta

import httpx
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    FSInputFile,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_URL = os.getenv("OPENAI_URL", "https://api.openai.com/v1/chat/completions")

LEMONFOX_API_KEY = os.getenv("LEMONFOX_API_KEY")
LEMONFOX_API_URL = os.getenv("LEMONFOX_API_URL")

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

DB_PATH = os.getenv("DB_PATH", "infinity_ai.db")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


# ---------- DB ----------

def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    lang TEXT DEFAULT 'ru',
    is_premium INTEGER DEFAULT 0,
    premium_until TEXT
)
"""
    )
    return conn


def get_user(user_id: int):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, lang, is_premium, premium_until FROM users WHERE user_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    if not row:
        cur.execute(
            "INSERT INTO users (user_id, lang, is_premium, premium_until) VALUES (?, 'ru', 0, NULL)",
            (user_id,),
        )
        conn.commit()
        conn.close()
        return {"user_id": user_id, "lang": "ru", "is_premium": False, "premium_until": None}
    conn.close()
    return {
        "user_id": row[0],
        "lang": row[1],
        "is_premium": bool(row[2]),
        "premium_until": row[3],
    }


def set_lang(user_id: int, lang: str):
    conn = db_connect()
    conn.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()


def set_premium(user_id: int, days: int = 30):
    conn = db_connect()
    premium_until = (datetime.utcnow() + timedelta(days=days)).isoformat()
    conn.execute(
        "UPDATE users SET is_premium = 1, premium_until = ? WHERE user_id = ?",
        (premium_until, user_id),
    )
    conn.commit()
    conn.close()


def is_premium(user_id: int) -> bool:
    u = get_user(user_id)
    if not u["is_premium"]:
        return False
    if not u["premium_until"]:
        return False
    try:
        dt = datetime.fromisoformat(u["premium_until"])
    except ValueError:
        return False
    return dt > datetime.utcnow()


# ---------- TEXTS ----------

TEXTS = {
    "start_choose_lang": {"ru": "Выберите язык:", "uz": "Tilni tanlang:"},
    "main_menu": {
        "ru": "Infinity AI — выберите действие:",
        "uz": "Infinity AI — amalni tanlang:",
    },
    "chat_prompt": {
        "ru": "Отправьте сообщение для ИИ.",
        "uz": "AI uchun xabar yuboring.",
    },
    "image_prompt": {
        "ru": "Опишите картинку (prompt), я сгенерирую изображение.",
        "uz": "Rasm tavsifini yozing (prompt), men tasvir yarataman.",
    },
    "no_premium_image": {
        "ru": "Генерация изображений доступна только по премиум-подписке.",
        "uz": "Rasm generatsiyasi faqat premium obuna uchun mavjud.",
    },
    "subscription_info": {
        "ru": "Подписка Infinity AI:\n\n"
              "• Бесплатно: чат с ИИ\n"
              "• Премиум: чат + картинки + приоритет.\n\n"
              "Выберите способ оплаты:",
        "uz": "Infinity AI obunasi:\n\n"
              "• Bepul: AI bilan chat\n"
              "• Premium: chat + rasmlar + ustun navbat.\n\n"
              "To'lov usulini tanlang:",
    },
    "ask_prompt_first": {
        "ru": "Сначала отправьте текст запроса.",
        "uz": "Avval matnli so'rov yuboring.",
    },
    "processing": {
        "ru": "Infinity AI обрабатывает ваш запрос…",
        "uz": "Infinity AI so'rovingizni qayta ishlamoqda…",
    },
    "error_ai": {
        "ru": "При обращении к ИИ произошла ошибка. Попробуйте ещё раз позже.",
        "uz": "AI bilan ishlashda xatolik yuz berdi. Keyinroq yana urinib ko'ring.",
    },
    "lemonfox_not_configured": {
        "ru": "Lemonfox API не настроен. Сообщите администратору.",
        "uz": "Lemonfox API sozlanmagan. Admin bilan bog'laning.",
    },
    "notify_admin_card": {
        "ru": "Сообщение об оплате отправлено администратору. Ожидайте активации.",
        "uz": "To'lov haqida xabar administratorga yuborildi. Aktivatsiyani kuting.",
    },
    "card_payment_request_admin": {
        "ru": "Пользователь сообщил об оплате на карту. "
              "Активировать премиум на 30 дней?",
        "uz": "Foydalanuvchi karta orqali to'lov qilganini xabar qildi. "
              "30 kunga premium yoqilsinmi?",
    },
    "premium_activated": {
        "ru": "Премиум-подписка активирована на 30 дней.",
        "uz": "Premium obuna 30 kunga faollashtirildi.",
    },
    "not_admin": {
        "ru": "У вас нет прав админа.",
        "uz": "Sizda admin huquqlari yo'q.",
    },
    "help": {
        "ru": "Я — Infinity AI.\n\n"
              "• 🤖 Чат с ИИ — ответы на вопросы\n"
              "• 🎨 Картинки — генерация изображений через Lemonfox\n"
              "• 💎 Подписка — управление тарифами\n\n"
              "Бот поддерживает русский и узбекский языки.",
        "uz": "Men — Infinity AI.\n\n"
              "• 🤖 AI bilan chat — savollarga javoblar\n"
              "• 🎨 Rasmlar — Lemonfox orqali tasvir yaratish\n"
              "• 💎 Obuna — tariflarni boshqarish\n\n"
              "Bot rus va o'zbek tillarini qo'llab-quvvatlaydi.",
    },
}


def t(user_lang: str, key: str) -> str:
    if key not in TEXTS:
        return ""
    if user_lang in TEXTS[key]:
        return TEXTS[key][user_lang]
    return TEXTS[key]["ru"]


# ---------- KEYBOARDS ----------

def lang_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Русский", callback_data="lang:ru")
    kb.button(text="O‘zbekcha", callback_data="lang:uz")
    kb.adjust(2)
    return kb.as_markup()


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if lang == "uz":
        kb.button(text="🤖 AI bilan chat", callback_data="menu:chat")
        kb.button(text="🎨 Rasmlar", callback_data="menu:image")
        kb.button(text="💎 Obuna", callback_data="menu:sub")
        kb.button(text="ℹ️ Yordam", callback_data="menu:help")
    else:
        kb.button(text="🤖 Чат с ИИ", callback_data="menu:chat")
        kb.button(text="🎨 Картинки", callback_data="menu:image")
        kb.button(text="💎 Подписка", callback_data="menu:sub")
        kb.button(text="ℹ️ Помощь", callback_data="menu:help")
    kb.adjust(2)
    return kb.as_markup()


def subscription_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if lang == "uz":
        kb.button(text="⭐ Telegram Stars", callback_data="sub:stars")
        kb.button(text="💳 Kartaga to'lov qildim", callback_data="sub:card")
    else:
        kb.button(text="⭐ Telegram Stars", callback_data="sub:stars")
        kb.button(text="💳 Оплатил на карту", callback_data="sub:card")
    kb.adjust(1)
    return kb.as_markup()


def admin_confirm_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Активировать 30 дней", callback_data=f"admin:approve:{user_id}")
    kb.button(text="❌ Отклонить", callback_data=f"admin:reject:{user_id}")
    kb.adjust(1)
    return kb.as_markup()


# ---------- AI FUNCTIONS ----------

async def ask_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(OPENAI_URL, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            logging.error("Unexpected OpenAI response: %s", data)
            raise RuntimeError("Invalid OpenAI response")


async def generate_image_lemonfox(prompt: str) -> bytes:
    if not LEMONFOX_API_URL or not LEMONFOX_API_KEY:
        raise RuntimeError("LEMONFOX_API_URL or LEMONFOX_API_KEY is not configured")
    headers = {
        "Authorization": f"Bearer {LEMONFOX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"prompt": prompt}
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(LEMONFOX_API_URL, headers=headers, json=payload)
        r.raise_for_status()
        content_type = r.headers.get("content-type", "")
        if content_type.startswith("image/"):
            return r.content
        data = r.json()
        logging.error("Unexpected Lemonfox response format: %s", data)
        raise RuntimeError("Unexpected Lemonfox response format")


# ---------- ROUTERS ----------

router = Router()


def get_lang(user_id: int) -> str:
    u = get_user(user_id)
    return u["lang"]


@router.message(CommandStart())
async def cmd_start(message: Message):
    get_user(message.from_user.id)
    await message.answer(TEXTS["start_choose_lang"]["ru"], reply_markup=lang_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def cb_set_lang(callback: CallbackQuery):
    lang = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    set_lang(user_id, lang)
    await callback.message.edit_text(
        t(lang, "main_menu"),
        reply_markup=main_menu_kb(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("menu:"))
async def cb_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_lang(user_id)
    action = callback.data.split(":", 1)[1]
    if action == "chat":
        await callback.message.edit_text(
            t(lang, "chat_prompt"),
            reply_markup=main_menu_kb(lang),
        )
    elif action == "image":
        await callback.message.edit_text(
            t(lang, "image_prompt"),
            reply_markup=main_menu_kb(lang),
        )
    elif action == "sub":
        await callback.message.edit_text(
            t(lang, "subscription_info"),
            reply_markup=subscription_kb(lang),
        )
    elif action == "help":
        await callback.message.edit_text(
            t(lang, "help"),
            reply_markup=main_menu_kb(lang),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("sub:"))
async def cb_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    lang = get_lang(user_id)
    action = callback.data.split(":", 1)[1]
    if action == "stars":
        if lang == "uz":
            text = "Telegram Stars orqali to'lov hali ulanmagan. Iltimos, admin bilan bog'laning."
        else:
            text = "Оплата через Telegram Stars ещё не подключена. Пожалуйста, свяжитесь с администратором."
        await callback.message.answer(text)
    elif action == "card":
        if ADMIN_ID:
            admin_text = (
                f"💳 Пользователь @{callback.from_user.username or callback.from_user.id} "
                f"(ID: {callback.from_user.id}) сообщил, что оплатил на карту.\n\n"
                f"{TEXTS['card_payment_request_admin']['ru']}"
            )
            await bot.send_message(
                ADMIN_ID,
                admin_text,
                reply_markup=admin_confirm_kb(callback.from_user.id),
            )
        await callback.message.answer(t(lang, "notify_admin_card"))
    await callback.answer()


@router.callback_query(F.data.startswith("admin:"))
async def cb_admin(callback: CallbackQuery):
    if ADMIN_ID == 0 or callback.from_user.id != ADMIN_ID:
        lang = get_lang(callback.from_user.id)
        await callback.answer(t(lang, "not_admin"), show_alert=True)
        return
    parts = callback.data.split(":")
    action = parts[1]
    target_user_id = int(parts[2])
    if action == "approve":
        set_premium(target_user_id, days=30)
        await callback.answer("OK", show_alert=False)
        await callback.message.edit_text(
            f"✅ Премиум активирован пользователю {target_user_id} на 30 дней."
        )
    elif action == "reject":
        await callback.answer("Отклонено", show_alert=False)
        await callback.message.edit_text("❌ Заявка отклонена.")
    else:
        await callback.answer("Unknown action", show_alert=True)


@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(t(lang, "help"), reply_markup=main_menu_kb(lang))


@router.message()
async def handle_message(message: Message, bot: Bot):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    text = (message.text or "").strip()
    if not text:
        await message.answer(t(lang, "ask_prompt_first"))
        return

    # простая эвристика: если пользователь явно просит "картинку", считаем это запросом на изображение
    lower = text.lower()
    is_image_query = any(
        key in lower
        for key in ["картинку", "картинка", "рисунок", "image:", "rasm", "surat"]
    )

    if is_image_query:
        if not is_premium(user_id):
            await message.answer(t(lang, "no_premium_image"))
            return
        await message.answer(t(lang, "processing"))
        try:
            img_bytes = await generate_image_lemonfox(text)
        except Exception as e:
            logging.exception("Error in Lemonfox: %s", e)
            await message.answer(t(lang, "error_ai"))
            return
        file_path = f"tmp_{user_id}.png"
        with open(file_path, "wb") as f:
            f.write(img_bytes)
        photo = FSInputFile(file_path)
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
        try:
            os.remove(file_path)
        except OSError:
            pass
    else:
        await message.answer(t(lang, "processing"))
        try:
            reply = await ask_openai(text)
        except Exception as e:
            logging.exception("Error in OpenAI: %s", e)
            await message.answer(t(lang, "error_ai"))
            return
        await message.answer(reply)


async def main():
    db_connect().close()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import uvloop
    uvloop.install()
    asyncio.run(main())
