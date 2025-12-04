from config import DEFAULT_LANG

TEXTS = {
    "start_title": {
        "ru": "Добро пожаловать в Infinity AI 🤖",
        "uz": "Infinity AI ga xush kelibsiz 🤖",
    },
    "start_desc": {
        "ru": "Этот бот объединяет лучшие ИИ: ChatGPT, Claude, Gemini, Grok, LLaMA, Midjourney-стиль, Suno-подобное аудио и многое другое.",
        "uz": "Bu bot eng kuchli AI modellarni birlashtiradi: ChatGPT, Claude, Gemini, Grok, LLaMA, Midjourney uslubidagi rasmlar, Suno-ga o‘xshash audio va boshqalar.",
    },
    "menu_main": {
        "ru": "Выберите раздел:",
        "uz": "Bo‘limni tanlang:",
    },
    "btn_text_ai": {
        "ru": "🧠 Текстовые ИИ",
        "uz": "🧠 Matnli AI",
    },
    "btn_image_ai": {
        "ru": "🎨 Картинки / Видео",
        "uz": "🎨 Rasm / Video",
    },
    "btn_audio_ai": {
        "ru": "🎧 Аудио ИИ (скоро)",
        "uz": "🎧 Audio AI (tez orada)",
    },
    "btn_profile": {
        "ru": "👤 Профиль",
        "uz": "👤 Profil",
    },
    "btn_subscription": {
        "ru": "💳 Подписка",
        "uz": "💳 Obuna",
    },
    "btn_language": {
        "ru": "🌐 Язык / Til",
        "uz": "🌐 Til / Язык",
    },

    "choose_language": {
        "ru": "Выберите язык интерфейса:",
        "uz": "Interfeys tilini tanlang:",
    },
    "lang_ru": {
        "ru": "Русский",
        "uz": "Rus tili",
    },
    "lang_uz": {
        "ru": "O‘zbekcha",
        "uz": "O‘zbekcha",
    },

    "text_ai_choose_model": {
        "ru": "Выберите текстовую модель ИИ:",
        "uz": "Matnli AI modelini tanlang:",
    },
    "image_ai_choose_model": {
        "ru": "Выберите модель для изображений:",
        "uz": "Rasmlar uchun modelni tanlang:",
    },

    "btn_model_chatgpt": {
        "ru": "ChatGPT",
        "uz": "ChatGPT",
    },
    "btn_model_claude": {
        "ru": "Claude",
        "uz": "Claude",
    },
    "btn_model_gemini": {
        "ru": "Gemini",
        "uz": "Gemini",
    },
    "btn_model_grok": {
        "ru": "Grok",
        "uz": "Grok",
    },
    "btn_model_llama": {
        "ru": "LLaMA (Groq)",
        "uz": "LLaMA (Groq)",
    },

    "btn_model_midjourney": {
        "ru": "Midjourney-style",
        "uz": "Midjourney uslubi",
    },
    "btn_model_flux": {
        "ru": "FLUX",
        "uz": "FLUX",
    },
    "btn_model_sdxl": {
        "ru": "SDXL Photoreal",
        "uz": "SDXL fotoreal",
    },
    "btn_model_seedream": {
        "ru": "Seedream 4.5",
        "uz": "Seedream 4.5",
    },
    "btn_model_upscale": {
        "ru": "Clarity Upscale",
        "uz": "Clarity Upscale",
    },

    "model_saved": {
        "ru": "Модель сохранена: {model}",
        "uz": "Model saqlandi: {model}",
    },

    "subscription_info": {
        "ru": "Ваш тариф: {tier}\nДействует до: {until}",
        "uz": "Tarifingiz: {tier}\nAmal qilish muddati: {until}",
    },
    "no_subscription": {
        "ru": "У вас пока нет активной подписки.",
        "uz": "Hozircha faol obunangiz yo‘q.",
    },

    "not_admin": {
        "ru": "У вас нет прав администратора.",
        "uz": "Sizda administrator huquqi yo‘q.",
    },
    "admin_panel": {
        "ru": "Админ-панель Infinity AI.\n\nКоманда для выдачи подписки:\n/give_sub user_id tier days\nПример:\n/give_sub 123456789 premium 30",
        "uz": "Infinity AI admin paneli.\n\nObuna berish buyrug‘i:\n/give_sub user_id tarif kunlar\nMasalan:\n/give_sub 123456789 premium 30",
    },

    "profile_info": {
        "ru": "👤 Профиль\n\nID: {user_id}\nЯзык: {lang}\nТекстовая модель: {text_model}\nМодель изображений: {image_model}\nПодписка: {sub}\nДо: {until}",
        "uz": "👤 Profil\n\nID: {user_id}\nTil: {lang}\nMatn modeli: {text_model}\nRasm modeli: {image_model}\nObuna: {sub}\nGacha: {until}",
    },

    "prompt_text_ai": {
        "ru": "Отправьте текстовое сообщение, и я обработаю его выбранной моделью ИИ.",
        "uz": "Tanlangan AI modeli bilan ishlov berish uchun matn yuboring.",
    },
    "prompt_image_ai": {
        "ru": "Отправьте описание картинки (prompt). Я сгенерирую изображение выбранной моделью.",
        "uz": "Rasm tavsifini (prompt) yuboring. Tanlangan model yordamida rasm yarataman.",
    },
    "processing_ai": {
        "ru": "⌛ Infinity AI обрабатывает ваш запрос...",
        "uz": "⌛ Infinity AI so‘rovingizni qayta ishlamoqda...",
    },
    "image_ready": {
        "ru": "Готово ✅",
        "uz": "Tayyor ✅",
    },
    "error_ai": {
        "ru": "Произошла ошибка при обращении к ИИ:\n{error}",
        "uz": "AI bilan ishlashda xatolik yuz berdi:\n{error}",
    },
}


def t(lang: str | None, key: str, **kwargs) -> str:
    if lang not in ("ru", "uz"):
        lang = DEFAULT_LANG
    template = TEXTS.get(key, {}).get(lang, "")
    if kwargs:
        return template.format(**kwargs)
    return template

