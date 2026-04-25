import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from gigachat_client import ask_gigachat

# Загрузка переменных окружения из .env файла
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("Ошибка: не найден токен TELEGRAM_BOT_TOKEN в файле .env")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Включить логирование
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    welcome_text = (
        "Привет! Я бот, использующий GigaChat для ответов на ваши вопросы.\n"
        "Просто напишите мне сообщение, и я постараюсь на него ответить."
    )
    await message.answer(welcome_text)


@dp.message()
async def handle_message(message: types.Message):
    """
    Обработчик обычных текстовых сообщений
    """
    # Проверяем, что сообщение содержит текст
    if not message.text:
        await message.reply("Пожалуйста, отправьте текстовое сообщение.")
        return
    
    # Отправляем сообщение пользователя в GigaChat
    try:
        # Показываем, что бот печатает
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # Отправляем сообщение в GigaChat
        response = ask_gigachat(message.text)
        
        # Отправляем ответ пользователю
        await message.reply(response)
    except Exception as e:
        # Логируем ошибку
        print(f"Ошибка при обработке сообщения: {e}")
        await message.reply("Произошла ошибка при обработке вашего запроса. Попробуйте позже.")


async def main():
    """
    Основная функция запуска бота
    """
    print("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())