import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Конфигурация ===
API_TOKEN = "8162554421:AAHFrwOptRMM5oiFCUrkiiQAw2glMvvsZLw"
CHANNEL_USERNAME = "@zalogautouz"
GSHEET_CREDENTIALS_FILE = 'creds.json'
GSHEET_NAME = "ZalogAvtoUz"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# === Google Sheets подключение ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEET_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(GSHEET_NAME).sheet1

# === Команда /start ===
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("\U0001F44B Привет! Я бот для поиска и публикации залоговых авто.\n\nКоманды:\n\U0001F50D /find — найти авто по фильтрам\n\U0001F4E3 /publish — опубликовать все в канал")

# === Команда /find — шаг 1: выбор марки ===
@dp.message_handler(commands=['find'])
async def find_cars(message: types.Message):
    rows = sheet.get_all_records()
    brands = sorted(set(row['Марка'].strip() for row in rows if row['Статус'] != ''))
    kb = InlineKeyboardMarkup(row_width=2)
    for brand in brands:
        kb.insert(InlineKeyboardButton(brand, callback_data=f"brand_{brand}"))
    kb.add(InlineKeyboardButton("Неважно", callback_data="brand_all"))
    await message.reply("Выбери марку авто:", reply_markup=kb)

# === Шаг 2 — выбор модели ===
@dp.callback_query_handler(lambda c: c.data.startswith("brand_"))
async def select_model(callback: types.CallbackQuery):
    selected_brand = callback.data[6:]
    rows = sheet.get_all_records()
    if selected_brand == "all":
        models = sorted(set(row['Модель'].strip() for row in rows if row['Статус'] != ''))
    else:
        models = sorted(set(row['Модель'].strip() for row in rows if row['Марка'] == selected_brand and row['Статус'] != ''))
    kb = InlineKeyboardMarkup(row_width=2)
    for model in models:
        kb.insert(InlineKeyboardButton(model, callback_data=f"model_{selected_brand}_{model}"))
    kb.add(InlineKeyboardButton("Неважно", callback_data=f"model_{selected_brand}_all"))
    await callback.message.edit_text("Выбери модель:", reply_markup=kb)

# === Шаг 3 — выбор года ===
@dp.callback_query_handler(lambda c: c.data.startswith("model_"))
async def select_year(callback: types.CallbackQuery):
    _, brand, model = callback.data.split("_", 2)
    rows = sheet.get_all_records()
    years = sorted(set(str(row['Год']).strip() for row in rows if row['Статус'] != ''))
    kb = InlineKeyboardMarkup(row_width=2)
    for year in years:
        kb.insert(InlineKeyboardButton(year, callback_data=f"year_{brand}_{model}_{year}"))
    kb.add(InlineKeyboardButton("Неважно", callback_data=f"year_{brand}_{model}_all"))
    await callback.message.edit_text("Выбери год выпуска:", reply_markup=kb)

# === Шаг 4 — выбор города ===
@dp.callback_query_handler(lambda c: c.data.startswith("year_"))
async def select_city(callback: types.CallbackQuery):
    _, brand, model, year = callback.data.split("_", 3)
    rows = sheet.get_all_records()
    cities = sorted(set(row['Город'].strip() for row in rows if row['Статус'] != ''))
    kb = InlineKeyboardMarkup(row_width=2)
    for city in cities:
        kb.insert(InlineKeyboardButton(city, callback_data=f"city_{brand}_{model}_{year}_{city}"))
    kb.add(InlineKeyboardButton("Неважно", callback_data=f"city_{brand}_{model}_{year}_all"))
    await callback.message.edit_text("Выбери город:", reply_markup=kb)

# === Шаг 5 — выбор цены ===
@dp.callback_query_handler(lambda c: c.data.startswith("city_"))
async def select_price(callback: types.CallbackQuery):
    _, brand, model, year, city = callback.data.split("_", 4)
    kb = InlineKeyboardMarkup(row_width=2)
    for limit in [100_000_000, 150_000_000, 200_000_000, 300_000_000, 500_000_000]:
        kb.insert(InlineKeyboardButton(f"до {limit} сум", callback_data=f"price_{brand}_{model}_{year}_{city}_{limit}"))
    kb.add(InlineKeyboardButton("Неважно", callback_data=f"price_{brand}_{model}_{year}_{city}_all"))
    await callback.message.edit_text("Укажи максимальную цену:", reply_markup=kb)

# === Шаг 6 — статус публикации ===
@dp.callback_query_handler(lambda c: c.data.startswith("price_"))
async def select_status(callback: types.CallbackQuery):
    _, brand, model, year, city, price = callback.data.split("_", 5)
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Только не опубликованные", callback_data=f"status_{brand}_{model}_{year}_{city}_{price}_new"),
        InlineKeyboardButton("Все", callback_data=f"status_{brand}_{model}_{year}_{city}_{price}_all")
    )
    await callback.message.edit_text("Показать только не опубликованные или все?", reply_markup=kb)

# === Показ результатов ===
@dp.callback_query_handler(lambda c: c.data.startswith("status_"))
async def show_results(callback: types.CallbackQuery):
    _, brand, model, year, city, price, status = callback.data.split("_", 6)
    rows = sheet.get_all_records()
    found = 0
    for row in rows:
        if brand != "all" and row['Марка'].lower() != brand.lower():
            continue
        if model != "all" and row['Модель'].lower() != model.lower():
            continue
        if year != "all" and str(row['Год']).strip() != year:
            continue
        if city != "all" and row['Город'].lower() != city.lower():
            continue
        if price != "all":
            try:
                p = int(str(row['Цена']).replace(" ", "").replace("млн", "").replace("сум", "").strip())
                if p > int(price):
                    continue
            except:
                continue
        if status == "new" and row['Статус'] == "✅ Опубликовано":
            continue

        try:
            full_model = f"{row['Марка']} {row['Модель']}"
            caption = f"🚗 <b>{full_model}</b>\n📍 {row['Город']}\n💰 {row['Цена']}"
            photo = row['Ссылка на фото'].split(",")[0]
            link = row.get("Ссылка на банк", "")
            phone = str(row.get("Телефон", "")).strip()
            tg = str(row.get("Телеграм", "")).strip()

            buttons = []
            if link:
                buttons.append(InlineKeyboardButton("🔗 Перейти", url=link))
            if phone.startswith("+"):
                buttons.append(InlineKeyboardButton("📞 Позвонить", url=f"https://t.me/share/url?url=tel:{phone}"))
            if tg:
                buttons.append(InlineKeyboardButton("📩 Написать", url=f"https://t.me/{tg.strip('@')}"))

            kb = InlineKeyboardMarkup(row_width=2).add(*buttons)
            await bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption=caption, reply_markup=kb, parse_mode="HTML")
            found += 1
        except Exception as e:
            logging.error(f"Ошибка при отправке: {e}")
            continue

    if found == 0:
        await callback.message.reply("❌ Объявлений не найдено по выбранным фильтрам.")

# === Команда /publish ===
@dp.message_handler(commands=['publish'])
async def publish_to_channel(message: types.Message):
    rows = sheet.get_all_records()
    count = 0

    for row in rows:
        if str(row.get("Статус", "")).strip().lower() == "готово":
            full_model = f"{row['Марка']} {row['Модель']}"
            city = row.get("Город", "")
            price = row.get("Цена", "")
            photo = row.get("Ссылка на фото", "").split(",")[0]
            phone = str(row.get("Телефон", "")).strip()
            tg = str(row.get("Телеграм", "")).strip()
            link = row.get("Ссылка на банк", "")

            caption = f"🚗 <b>{full_model}</b>\n📍 {city}\n💰 {price} млн"

            buttons = []
            if link:
                buttons.append(InlineKeyboardButton("🔗 Перейти", url=link))
            if phone.startswith("+") or phone.startswith("998"):
                buttons.append(InlineKeyboardButton("📞 Позвонить", url=f"https://t.me/share/url?url=tel:{phone}"))
            if tg:
                buttons.append(InlineKeyboardButton("✉️ Написать", url=f"https://t.me/{tg.lstrip('@')}"))

            keyboard = InlineKeyboardMarkup(row_width=2).add(*buttons)

            try:
                await bot.send_photo(chat_id=CHANNEL_USERNAME, photo=photo, caption=caption, parse_mode="HTML", reply_markup=keyboard)
                count += 1
            except Exception as e:
                await message.reply(f"❗️ Ошибка публикации: {e}")

    await message.reply(f"✅ Опубликовано {count} объявлений в канал.")

# === Запуск ===
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
