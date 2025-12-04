from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from db import get_or_create_user, set_text_model
from localization import t
from model_presets import TEXT_MODEL_MAP
from utils.api_client import smart_client

router = Router(name="text_ai")


@router.callback_query(F.data.startswith("model:text:"))
async def on_set_text_model_callback(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id)
    lang = user.language

    _, _, key = callback.data.split(":")  # model:text:chatgpt
    set_text_model(callback.from_user.id, key)

    label_map = {
        "chatgpt": t(lang, "btn_model_chatgpt"),
        "claude": t(lang, "btn_model_claude"),
        "gemini": t(lang, "btn_model_gemini"),
        "grok": t(lang, "btn_model_grok"),
        "llama": t(lang, "btn_model_llama"),
    }
    label = label_map.get(key, key)

    await callback.answer(t(lang, "model_saved", model=label), show_alert=True)

    # Подсказка пользователю
    await callback.message.edit_text(t(lang, "prompt_text_ai"))
    

@router.message(F.text & ~F.via_bot)
async def handle_text_message(message: Message):
    """
    Базовая логика: любой текст → выбранная текстовая модель.
    Если потом захочешь добавить режимы (чат/команда), можно расширить.
    """
    user = get_or_create_user(message.from_user.id)
    lang = user.language

    prompt = message.text.strip()
    if not prompt:
        return

    await message.answer(t(lang, "processing_ai"))

    text_key = user.text_model or "chatgpt"
    model = TEXT_MODEL_MAP.get(text_key, "gpt-4o-mini")

    try:
        answer = await smart_client.call_text(model=model, prompt=prompt)
        await message.answer(answer)
    except Exception as e:
        await message.answer(t(lang, "error_ai", error=str(e)))
