import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from cert_config import CERT_PATH

try:
    from gigachat import GigaChat
except ImportError:
    print("Ошибка: библиотека gigachat не установлена.")
    print("Установите её командой: pip install gigachat")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GIGACHAT_API_KEY")
SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

if not API_KEY:
    print("Ошибка: не найден ключ GIGACHAT_API_KEY в файле .env")
    sys.exit(1)


def create_client():
    return GigaChat(
        credentials=API_KEY,
        scope=SCOPE,
        ca_bundle_file=CERT_PATH,
        timeout=60,
    )


def ask_gigachat(user_message):
    payload = {
        "model": "GigaChat-2",
        "messages": [{"role": "user", "content": user_message}],
        "stream": False,
    }

    try:
        print("[DEBUG] Создаем клиент")
        with create_client() as client:
            print("[DEBUG] Отправляем запрос")
            response = client.chat(payload)
            print("[DEBUG] Ответ получен")
            return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при обращении к GigaChat: {e}")
        raise


def main():
    print("Консольный клиент GigaChat. Введите 'выход' для завершения работы.")

    try:
        while True:
            user_input = input("\nВаш вопрос: ")

            if user_input.lower() in ["выход", "exit", "quit"]:
                print("До свидания!")
                break

            if not user_input.strip():
                print("Пожалуйста, введите ваш вопрос.")
                continue

            try:
                print("Отправляем запрос в GigaChat...")
                answer = ask_gigachat(user_input)
                print(f"\nОтвет GigaChat:\n{answer}")
            except Exception as error:
                print(f"Ошибка при запросе к GigaChat API: {error}")
                raise
    except KeyboardInterrupt:
        print("\nДо свидания!")


if __name__ == "__main__":
    main()