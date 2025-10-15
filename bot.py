import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()  # загружает .env если есть

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN environment variable is not set")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ads = []
discounts = [
    {"title": "Кофейня “Beans”", "desc": "10% для студентов по студенческому!"},
    {"title": "Копи-центр “Print+”", "desc": "15% скидка на печать дипломов."},
    {"title": "Кофейня “Coffee Like”", "desc": "10% для студентов по студенческому!"}
]

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📢 Объявления", "💼 Добавить объявление")
    keyboard.add("🎓 Скидки", "👤 Профиль")
    keyboard.add("ℹ️ О проекте")
    return keyboard

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("👋 Привет! Это UniLink — бот для студентов Бузулука.
Выбери раздел:", reply_markup=main_keyboard())

@dp.message_handler(lambda message: message.text == "📢 Объявления")
async def show_ads(message: types.Message):
    if not ads:
        await message.answer("Пока объявлений нет. Добавь своё!")
    else:
        text = "\n\n".join([f"📌 {a['title']}\n{a['desc']}\nКонтакт: {a['contact']}" for a in ads])
        await message.answer(text)

@dp.message_handler(lambda message: message.text == "💼 Добавить объявление")
async def add_ad(message: types.Message):
    await message.answer("Отправь объявление в формате:\nНазвание | Описание | Контакт")

@dp.message_handler(lambda message: "|" in message.text)
async def save_ad(message: types.Message):
    parts = message.text.split("|")
    if len(parts) == 3:
        ads.append({"title": parts[0].strip(), "desc": parts[1].strip(), "contact": parts[2].strip()})
        await message.answer("✅ Объявление добавлено!")
    else:
        await message.answer("❌ Формат неверный. Пример: Название | Описание | Контакт")

@dp.message_handler(lambda message: message.text == "🎓 Скидки")
async def show_discounts(message: types.Message):
    text = "\n\n".join([f"🎁 {d['title']}\n{d['desc']}" for d in discounts])
    await message.answer(text)

@dp.message_handler(lambda message: message.text == "👤 Профиль")
async def profile(message: types.Message):
    await message.answer(f"👋 Привет, {message.from_user.first_name}! Здесь будет информация о твоих объявлениях и скидках.")

@dp.message_handler(lambda message: message.text == "ℹ️ О проекте")
async def about(message: types.Message):
    await message.answer("🎓 UniLink — сервис для студентов Бузулука. Здесь можно обмениваться материалами, искать помощь и узнавать о скидках от локальных партнёров.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
