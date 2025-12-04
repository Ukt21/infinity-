# Логические ключи → реальные имена моделей у провайдеров

# Текстовые модели
TEXT_MODEL_MAP = {
    # OpenAI
    "chatgpt": "gpt-4o-mini",  # или gpt-4o

    # OpenRouter (имена уточняются по документации OpenRouter)
    "claude": "anthropic/claude-3.5-sonnet",
    "gemini": "google/gemini-2.0-flash-exp",
    "grok": "x-ai/grok-beta",

    # Groq (через наш префикс groq- в SmartAIClient)
    "llama": "groq-llama-3-70b",
}

# Визуальные модели (имена условные, нужно подставить реальные из LemonFox)
IMAGE_MODEL_MAP = {
    "midjourney": "midjourney-v6",
    "flux": "flux-1.1-pro",
    "sdxl": "sdxl-photoreal",
    "seedream": "seedream-4.5",
    "upscale": "clarity-upscale",
}
