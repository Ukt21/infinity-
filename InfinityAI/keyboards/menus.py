from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import t


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_text_ai"), callback_data="menu:text_ai")],
            [InlineKeyboardButton(text=t(lang, "btn_image_ai"), callback_data="menu:image_ai")],
            [InlineKeyboardButton(text=t(lang, "btn_audio_ai"), callback_data="menu:audio_ai")],
            [
                InlineKeyboardButton(text=t(lang, "btn_profile"), callback_data="menu:profile"),
                InlineKeyboardButton(text=t(lang, "btn_subscription"), callback_data="menu:subscription"),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_language"), callback_data="menu:language")],
        ]
    )


def language_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "lang_ru"), callback_data="lang:ru"),
                InlineKeyboardButton(text=t(lang, "lang_uz"), callback_data="lang:uz"),
            ]
        ]
    )


def text_models_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_model_chatgpt"), callback_data="model:text:chatgpt"),
                InlineKeyboardButton(text=t(lang, "btn_model_claude"), callback_data="model:text:claude"),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_model_gemini"), callback_data="model:text:gemini"),
                InlineKeyboardButton(text=t(lang, "btn_model_grok"), callback_data="model:text:grok"),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_model_llama"), callback_data="model:text:llama"),
            ],
        ]
    )


def image_models_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_model_midjourney"), callback_data="model:image:midjourney"),
                InlineKeyboardButton(text=t(lang, "btn_model_flux"), callback_data="model:image:flux"),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_model_sdxl"), callback_data="model:image:sdxl"),
                InlineKeyboardButton(text=t(lang, "btn_model_seedream"), callback_data="model:image:seedream"),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_model_upscale"), callback_data="model:image:upscale"),
            ],
        ]
    )
