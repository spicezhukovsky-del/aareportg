import asyncio
import os
import sys
import logging

from aiogram import Dispatcher, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, FSInputFile
)

from config_reader import get_config, BotConfig

dp = Dispatcher()

@dp.message(Command("star"))
async def cmd_stars(message: Message):
    kb = [
        [KeyboardButton(text="Сгенерировать отчеты для всех школ")],
        [KeyboardButton(text="Что в разработке?")]
    ]
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )
    await message.answer("Что делаем?", reply_markup=keyboard)

@dp.message(F.text.lower() == "сгенерировать отчеты для всех школ")
async def start_generator(message: Message):
    # 1. Сообщаем о начале долгого процесса
    await message.reply("Генерация отчётов началась, пожалуйста, подождите...")

    try:
        # 2. Запускаем тяжёлую синхронную функцию в отдельном потоке
        generated_files = await asyncio.to_thread(report_generator)

        # 3. Проверка на случай, если функция вернула пустой список
        if not generated_files:
            await message.reply("Отчёты не были созданы (список файлов пуст).")
            return

        await message.reply(f"Генерация завершена! Начинаю отправку {len(generated_files)} файлов...")

        # 4. Отправляем каждый файл
        for file_path in generated_files:
            if os.path.exists(file_path):
                document = FSInputFile(file_path)
                await message.answer_document(document)

                # 5. Удаляем файл после успешной отправки, чтобы не засорять диск
                os.remove(file_path)

                # 6. ВАЖНО: Небольшая пауза между отправками
                await asyncio.sleep(0.5)
            else:
                await message.reply(f"Файл не найден на диске: {file_path}")

        await message.reply("Все отчёты успешно сгенерированы и отправлены!")

    except Exception as e:
        await message.reply(f"Ошибка при генерации отчётов: {str(e)}")



async def main():
    bot_config = get_config(model=BotConfig, root_key="bot")
    bot = Bot(bot_config.token.get_secret_value())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
