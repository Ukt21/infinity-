import httpx
from typing import Any, Dict

from config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    LEMONFOX_API_KEY,
    LEMONFOX_BASE_URL,
)


class SmartAIClient:
    """
    Универсальный клиент для:
    - текстовых моделей (OpenAI / Groq / OpenRouter)
    - изображений (LemonFox)
    - аудио (LemonFox, заготовка)
    """

    # ---------- ТЕКСТ ----------

    async def call_text(self, model: str, prompt: str, extra: Dict[str, Any] | None = None) -> str:
        """
        model:
          - 'gpt-4o-mini' / 'gpt-4o' -> OpenAI
          - 'groq-llama-3-70b'       -> Groq (логический, внутри конвертируем)
          - 'anthropic/...'          -> OpenRouter
          - 'google/...'             -> OpenRouter
          - 'x-ai/grok-beta'         -> OpenRouter
        """
        extra = extra or {}

        # OpenAI
        if model.startswith("gpt-"):
            return await self._call_openai_chat(model, prompt, extra)

        # Groq (наш convention: model начинается с 'groq-')
        if model.startswith("groq-"):
            real_model = model.replace("groq-", "")
            return await self._call_groq_chat(real_model, prompt, extra)

        # Всё остальное через OpenRouter
        return await self._call_openrouter_chat(model, prompt, extra)

    async def _call_openai_chat(self, model: str, prompt: str, extra: Dict[str, Any]) -> str:
        url = f"{OPENAI_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }
        payload.update(extra)

        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()

        return data["choices"][0]["message"]["content"]

    async def _call_groq_chat(self, model: str, prompt: str, extra: Dict[str, Any]) -> str:
        url = f"{GROQ_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }
        payload.update(extra)

        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()

        return data["choices"][0]["message"]["content"]

    async def _call_openrouter_chat(self, model: str, prompt: str, extra: Dict[str, Any]) -> str:
        url = f"{OPENROUTER_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://infinity-ai-bot.example",
            "X-Title": "Infinity AI Telegram Bot",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }
        payload.update(extra)

        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()

        return data["choices"][0]["message"]["content"]

    # ---------- ИЗОБРАЖЕНИЯ ----------

    async def generate_image(self, model: str, prompt: str, extra: Dict[str, Any] | None = None) -> bytes:
        """
        Генерация изображения через LemonFox.
        model: имя модели на стороне LemonFox (см. документацию).
        Возвращает bytes изображения.
        """
        if not LEMONFOX_API_KEY:
            raise RuntimeError("LEMONFOX_API_KEY не задан")

        extra = extra or {}
        url = f"{LEMONFOX_BASE_URL}/image/generate"  # проверить по документации LemonFox
        headers = {
            "Authorization": f"Bearer {LEMONFOX_API_KEY}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
        }
        payload.update(extra)

        async with httpx.AsyncClient(timeout=180.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()

            # Вариант 1: API возвращает бинарный контент
            if r.headers.get("Content-Type", "").startswith("image/"):
                return r.content

            # Вариант 2: API возвращает JSON c URL → нужно скачать
            data = r.json()
            image_url = data.get("image_url") or data.get("url")
            if not image_url:
                raise RuntimeError("LemonFox не вернул image_url")

            r_img = await client.get(image_url)
            r_img.raise_for_status()
            return r_img.content

    # ---------- АУДИО (заготовка) ----------

    async def generate_audio(self, model: str, prompt: str, extra: Dict[str, Any] | None = None) -> bytes:
        """
        Заготовка под Suno / ElevenLabs через LemonFox.
        """
        if not LEMONFOX_API_KEY:
            raise RuntimeError("LEMONFOX_API_KEY не задан")

        extra = extra or {}
        url = f"{LEMONFOX_BASE_URL}/audio/generate"  # проверить по документации LemonFox
        headers = {
            "Authorization": f"Bearer {LEMONFOX_API_KEY}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
        }
        payload.update(extra)

        async with httpx.AsyncClient(timeout=300.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()

            if r.headers.get("Content-Type", "").startswith("audio/"):
                return r.content

            data = r.json()
            audio_url = data.get("audio_url") or data.get("url")
            if not audio_url:
                raise RuntimeError("LemonFox не вернул audio_url")

            r_audio = await client.get(audio_url)
            r_audio.raise_for_status()
            return r_audio.content


smart_client = SmartAIClient()

