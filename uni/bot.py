import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📢 Объявления", "💼 Услуги", "🎓 Скидки"]
    keyboard.add(*buttons)
    await message.answer("👋 Привет! Это UniLink — бот для студентов Бузулука.
Выбери нужный раздел 👇", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📢 Объявления")
async def announcements(message: types.Message):
    await message.answer("Здесь будут объявления студентов 🎓")

@dp.message_handler(lambda message: message.text == "💼 Услуги")
async def services(message: types.Message):
    await message.answer("Здесь будут услуги студентов 💼")

@dp.message_handler(lambda message: message.text == "🎓 Скидки")
async def discounts(message: types.Message):
    await message.answer("Здесь появятся скидки от партнёров 🎁")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
