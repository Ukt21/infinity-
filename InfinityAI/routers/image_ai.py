import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from db import get_or_create_user, set_image_model
from localization import t
from model_presets import IMAGE_MODEL_MAP
from utils.api_client import smart_client

router = Router(name="image_ai")


@router.callback_query(F.data.startswith("model:image:"))
async def on_set_image_model_callback(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id)
    lang = user.language

    _, _, key = callback.data.split(":")  # model:image:midjourney
    set_image_model(callback.from_user.id, key)

    label_map = {
        "midjourney": t(lang, "btn_model_midjourney"),
        "flux": t(lang, "btn_model_flux"),
        "sdxl": t(lang, "btn_model_sdxl"),
        "seedream": t(lang, "btn_model_seedream"),
        "upscale": t(lang, "btn_model_upscale"),
    }
    label = label_map.get(key, key)

    await callback.answer(t(lang, "model_saved", model=label), show_alert=True)
    await callback.message.edit_text(t(lang, "prompt_image_ai"))


@router.message(F.text.startswith("/img"))
async def cmd_img(message: Message):
    """
    /img <описание> — генерация изображения через выбранную модель.
    """
    user = get_or_create_user(message.from_user.id)
    lang = user.language

    prompt = message.text.replace("/img", "", 1).strip()
    if not prompt:
        await message.answer(t(lang, "prompt_image_ai"))
        return

    await message.answer(t(lang, "processing_ai"))

    image_key = user.image_model or "midjourney"
    model = IMAGE_MODEL_MAP.get(image_key, "flux-1.1-pro")

    try:
        img_bytes = await smart_client.generate_image(model=model, prompt=prompt)

        os.makedirs("tmp_images", exist_ok=True)
        filename = f"tmp_images/{uuid.uuid4().hex}.png"
        with open(filename, "wb") as f:
            f.write(img_bytes)

        await message.answer_photo(
            FSInputFile(filename),
            caption=t(lang, "image_ready"),
        )
        os.remove(filename)
    except Exception as e:
        await message.answer(t(lang, "error_ai", error=str(e)))
