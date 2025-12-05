from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import t


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 " + t(lang, "btn_text_ai"), callback_data="menu:text_ai")],
            [InlineKeyboardButton(text="🎨 " + t(lang, "btn_image_ai"), callback_data="menu:image_ai")],
            [InlineKeyboardButton(text="🎧 " + t(lang, "btn_audio_ai"), callback_data="menu:audio_ai")],
            [
                InlineKeyboardButton(text="👤 " + t(lang, "btn_profile"), callback_data="menu:profile"),
                InlineKeyboardButton(text="💳 " + t(lang, "btn_subscription"), callback_data="menu:subscription"),
            ],
            [InlineKeyboardButton(text="🌐 " + t(lang, "btn_language"), callback_data="menu:language")],
        ]
    )


def back_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")]
        ]
    )


def language_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "lang_ru"), callback_data="lang:ru"),
                InlineKeyboardButton(text=t(lang, "lang_uz"), callback_data="lang:uz"),
            ],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")]
        ]
    )


def text_models_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ChatGPT 🧠", callback_data="model:text:chatgpt"),
                InlineKeyboardButton(text="Claude ✨", callback_data="model:text:claude"),
            ],
            [
                InlineKeyboardButton(text="Gemini ⚡️", callback_data="model:text:gemini"),
                InlineKeyboardButton(text="Grok 🔥", callback_data="model:text:grok"),
            ],
            [
                InlineKeyboardButton(text="LLaMA 🚀", callback_data="model:text:llama"),
            ],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")]
        ]
    )


def image_models_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Midjourney 🎨", callback_data="model:image:midjourney"),
                InlineKeyboardButton(text="FLUX ⚡️", callback_data="model:image:flux"),
            ],
            [
                InlineKeyboardButton(text="SDXL 📸", callback_data="model:image:sdxl"),
                InlineKeyboardButton(text="Seedream 🧊", callback_data="model:image:seedream"),
            ],
            [
                InlineKeyboardButton(text="Upscale 🔍", callback_data="model:image:upscale"),
            ],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")]
        ]
    )

