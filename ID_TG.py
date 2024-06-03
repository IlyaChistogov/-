import asyncio
from telegram import Bot

# Вставьте токен вашего бота здесь
TOKEN = '6476840022:AAGjYn2cYnCpNE0KcJHkuPvU8DIKTKQGkWI'

async def main():
    bot = Bot(TOKEN)
    try:
        # Асинхронно получаем информацию о боте
        bot_info = await bot.get_me()
        # Выводим ID бота
        print(f"Bot ID: {bot_info.id}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Очистка: явно закрываем асинхронные сессии и соединения
        await bot.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
