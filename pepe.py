import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession

# ===== НАСТРОЙКИ =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

CHANNEL_ID = -1003971374938           

PROXY_URL = 'socks5://45.144.49.156:1080'
# ==================================

MESSAGE_TEXT = (
    "Привет, увидел твою заявку! 👋\n\n"
    "Если хочешь забрать бесплатный подарок, перешли пост к себе в тгк "
    "(если нету тгк, то своим 5 друзьям) который находится тут @doomfd "
    "И отправь скриншоты @doom_73, он выдаст тебе рандомный подарок "
    "(от 15 звезд до 100)!"
)

logging.basicConfig(level=logging.INFO)


async def main():
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Кидай пост в свой тгк и лутай подарок!")
    
    @dp.chat_join_request()
    async def on_join_request(update: types.ChatJoinRequest):
        if update.chat.id == CHANNEL_ID:
            user = update.from_user
            try:
                await bot.send_message(chat_id=user.id, text=MESSAGE_TEXT)
                logging.info(f"✅ Сообщение отправлено пользователю {user.id} ({user.full_name})")
            except Exception as e:
                logging.error(f"❌ Не удалось отправить сообщение {user.id}: {e}")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())