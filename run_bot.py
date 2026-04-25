#!/usr/bin/env python3
"""
Скрипт для запуска Telegram-бота на базе GigaChat
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from telegram_bot import main

if __name__ == "__main__":
    print("Запуск Telegram-бота на базе GigaChat...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)