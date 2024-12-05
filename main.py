import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
from config import TOKEN


translator = Translator()

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Привет! Я ваш бот.")


# Обработчик сообщений с фотографиями
@dp.message(F.photo)
async def handle_photo(message: Message):
    if not os.path.exists('img'):
        os.makedirs('img')

    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_path = f'img/{photo.file_id}.jpg'
    await bot.download_file(file_info.file_path, photo_path)
    await message.answer("Я сохранил ваш файл, он в надежных руках!")

# Команда для отправки голосового сообщения
@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("game_over_sound.ogg")
    await message.answer_voice(voice)

# Переводчик
@dp.message(F.text)
async def handle_text(message: Message):
    translated_text = translator.translate(message.text, src='auto', dest='en').text
    await message.answer(translated_text)


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())