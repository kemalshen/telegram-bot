import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import os

from config import BOT_TOKEN, CHANNEL_USERNAME, LOGGING_CONFIG
from simple_database import SimpleDatabaseManager
from post_formatter import PostFormatter

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Initialize database
db = SimpleDatabaseManager()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Welcome message and main menu"""
    welcome_text = (
        "🚗 <b>Добро пожаловать в ZalogAvtoUz Bot!</b>\n\n"
        "Я помогу вам найти и опубликовать залоговые автомобили.\n\n"
        "<b>Доступные команды:</b>\n"
        "🔍 /find — найти автомобили по фильтрам\n"
        "📝 /publish — добавить новый автомобиль\n"
        "📊 /stats — статистика базы данных\n"
        "📋 /help — справка по командам\n\n"
        "Выберите действие:"
    )
    
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔍 Найти авто", callback_data="action_find"),
        InlineKeyboardButton("📝 Добавить авто", callback_data="action_publish")
    )
    kb.add(
        InlineKeyboardButton("📊 Статистика", callback_data="action_stats"),
        InlineKeyboardButton("📋 Помощь", callback_data="action_help")
    )
    
    await message.reply(welcome_text, reply_markup=kb, parse_mode="HTML")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Help command"""
    help_text = (
        "📋 <b>Справка по командам</b>\n\n"
        "<b>Основные команды:</b>\n"
        "🔍 /find — поиск автомобилей по марке, модели, году, городу и цене\n"
        "📝 /publish — добавление нового автомобиля в базу данных\n"
        "📊 /stats — просмотр статистики базы данных\n"
        "📋 /help — эта справка\n\n"
        "<b>Как использовать:</b>\n"
        "1. Для поиска используйте /find и следуйте инструкциям\n"
        "2. Для добавления автомобиля используйте /publish\n"
        "3. Все добавленные автомобили автоматически публикуются в канале\n\n"
        "По всем вопросам обращайтесь к администратору."
    )
    
    await message.reply(help_text, parse_mode="HTML")

@dp.message_handler(commands=['stats'])
async def stats_command(message: types.Message):
    """Show database statistics"""
    try:
        cars = db.get_all_cars()
        brands = db.get_unique_values('Марка')
        cities = db.get_unique_values('Город')
        
        stats_text = (
            "📊 <b>Статистика базы данных</b>\n\n"
            f"🚗 <b>Всего автомобилей:</b> {len(cars)}\n"
            f"🏭 <b>Марок:</b> {len(brands)}\n"
            f"🏙️ <b>Городов:</b> {len(cities)}\n\n"
            f"<b>Популярные марки:</b>\n"
        )
        
        # Count brands
        brand_counts = {}
        for car in cars:
            brand = car.get('Марка', '')
            if brand:
                brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        # Show top 5 brands
        top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for brand, count in top_brands:
            stats_text += f"• {brand}: {count} авто\n"
        
        await message.reply(stats_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await message.reply("❌ Ошибка при получении статистики")

@dp.message_handler(commands=['find'])
async def find_command(message: types.Message):
    """Start the search process"""
    await start_search(message)

async def start_search(message: types.Message):
    """Start the search process with brand selection"""
    brands = db.get_unique_values('Марка')
    
    kb = InlineKeyboardMarkup(row_width=2)
    for brand in brands[:8]:  # Limit to 8 buttons
        kb.insert(InlineKeyboardButton(brand, callback_data=f"search_brand_{brand}"))
    kb.add(InlineKeyboardButton("Все марки", callback_data="search_brand_all"))
    
    await message.reply(
        "🔍 <b>Поиск автомобилей</b>\n\n"
        "Выберите марку автомобиля:",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data.startswith("search_brand_"))
async def handle_search_brand(callback_query: types.CallbackQuery):
    """Handle brand selection in search"""
    brand = callback_query.data.replace("search_brand_", "")
    
    if brand == "all":
        models = db.get_unique_values('Модель')
    else:
        # Get models for this brand
        cars = db.get_cars_by_filters({'brand': brand})
        models = list(set(car.get('Модель', '') for car in cars if car.get('Модель')))
    
    kb = InlineKeyboardMarkup(row_width=2)
    for model in models[:8]:
        kb.insert(InlineKeyboardButton(model, callback_data=f"search_model_{brand}_{model}"))
    kb.add(InlineKeyboardButton("Все модели", callback_data=f"search_model_{brand}_all"))
    
    await callback_query.message.edit_text(
        f"🔍 <b>Поиск: {brand if brand != 'all' else 'Все марки'}</b>\n\n"
        "Выберите модель:",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data.startswith("search_model_"))
async def handle_search_model(callback_query: types.CallbackQuery):
    """Handle model selection in search"""
    _, brand, model = callback_query.data.split("_", 2)
    
    # Get years
    cars = db.get_cars_by_filters({'brand': brand, 'model': model})
    years = list(set(str(car.get('Год', '')) for car in cars if car.get('Год')))
    years.sort()
    
    kb = InlineKeyboardMarkup(row_width=3)
    for year in years[:9]:
        kb.insert(InlineKeyboardButton(year, callback_data=f"search_year_{brand}_{model}_{year}"))
    kb.add(InlineKeyboardButton("Все годы", callback_data=f"search_year_{brand}_{model}_all"))
    
    await callback_query.message.edit_text(
        f"🔍 <b>Поиск: {brand} {model}</b>\n\n"
        "Выберите год:",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data.startswith("search_year_"))
async def handle_search_year(callback_query: types.CallbackQuery):
    """Handle year selection in search"""
    _, brand, model, year = callback_query.data.split("_", 3)
    
    # Get cities
    cars = db.get_cars_by_filters({'brand': brand, 'model': model, 'year': year})
    cities = list(set(car.get('Город', '') for car in cars if car.get('Город')))
    cities.sort()
    
    kb = InlineKeyboardMarkup(row_width=2)
    for city in cities[:6]:
        kb.insert(InlineKeyboardButton(city, callback_data=f"search_city_{brand}_{model}_{year}_{city}"))
    kb.add(InlineKeyboardButton("Все города", callback_data=f"search_city_{brand}_{model}_{year}_all"))
    
    await callback_query.message.edit_text(
        f"🔍 <b>Поиск: {brand} {model} {year}</b>\n\n"
        "Выберите город:",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data.startswith("search_city_"))
async def handle_search_city(callback_query: types.CallbackQuery):
    """Handle city selection in search"""
    _, brand, model, year, city = callback_query.data.split("_", 4)
    
    # Get price ranges
    kb = InlineKeyboardMarkup(row_width=2)
    price_ranges = [
        (0, 100_000_000, "до 100 млн"),
        (100_000_000, 150_000_000, "100-150 млн"),
        (150_000_000, 200_000_000, "150-200 млн"),
        (200_000_000, 300_000_000, "200-300 млн"),
        (300_000_000, 500_000_000, "300-500 млн"),
        (500_000_000, float('inf'), "от 500 млн")
    ]
    
    for min_price, max_price, label in price_ranges:
        kb.insert(InlineKeyboardButton(
            label, 
            callback_data=f"search_price_{brand}_{model}_{year}_{city}_{max_price}"
        ))
    kb.add(InlineKeyboardButton("Любая цена", callback_data=f"search_price_{brand}_{model}_{year}_{city}_all"))
    
    await callback_query.message.edit_text(
        f"🔍 <b>Поиск: {brand} {model} {year} {city}</b>\n\n"
        "Выберите ценовой диапазон:",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data.startswith("search_price_"))
async def handle_search_price(callback_query: types.CallbackQuery):
    """Handle price selection and show results"""
    _, brand, model, year, city, price = callback_query.data.split("_", 5)
    
    # Build filters
    filters = {
        'brand': brand,
        'model': model,
        'year': year,
        'city': city,
        'max_price': price
    }
    
    # Get filtered cars
    cars = db.get_cars_by_filters(filters)
    
    if not cars:
        await callback_query.message.edit_text(
            "❌ <b>По вашему запросу ничего не найдено</b>\n\n"
            "Попробуйте изменить параметры поиска.",
            parse_mode="HTML"
        )
        return
    
    # Show results
    results_text = PostFormatter.format_search_results(cars, filters)
    
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔍 Новый поиск", callback_data="new_search"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    await callback_query.message.edit_text(results_text, reply_markup=kb, parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == "new_search")
async def new_search(callback_query: types.CallbackQuery):
    """Start a new search"""
    await start_search(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == "main_menu")
async def main_menu(callback_query: types.CallbackQuery):
    """Return to main menu"""
    await start_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data.startswith("action_"))
async def handle_main_actions(callback_query: types.CallbackQuery):
    """Handle main menu actions"""
    action = callback_query.data.replace("action_", "")
    
    if action == "find":
        await start_search(callback_query.message)
    elif action == "publish":
        await callback_query.message.reply(
            "📝 <b>Добавление автомобиля</b>\n\n"
            "Эта функция будет доступна после подключения к Google Sheets.\n"
            "Пока что используйте команду /find для поиска автомобилей.",
            parse_mode="HTML"
        )
    elif action == "stats":
        await stats_command(callback_query.message)
    elif action == "help":
        await help_command(callback_query.message)

@dp.message_handler(commands=['publish_all'])
async def publish_all_command(message: types.Message):
    """Publish all unpublished cars to channel"""
    try:
        unpublished_cars = db.get_unpublished_cars()
        
        if not unpublished_cars:
            await message.reply("✅ Все автомобили уже опубликованы!")
            return
        
        published_count = 0
        
        for car in unpublished_cars:
            try:
                # Format the post
                post_data = PostFormatter.format_car_post(car)
                
                # Send to channel
                await bot.send_photo(
                    chat_id=CHANNEL_USERNAME,
                    photo=post_data['photo_url'],
                    caption=post_data['text'],
                    reply_markup=post_data['buttons'],
                    parse_mode="HTML"
                )
                
                # Update status
                db.update_car_status(car['row_index'], '✅ Опубликовано')
                published_count += 1
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error publishing car {car.get('Марка', '')} {car.get('Модель', '')}: {e}")
                continue
        
        await message.reply(f"✅ Опубликовано {published_count} автомобилей в канал!")
        
    except Exception as e:
        logger.error(f"Error in publish_all: {e}")
        await message.reply("❌ Ошибка при публикации автомобилей")

if __name__ == '__main__':
    logger.info("Starting ZalogAvtoUz Bot (Simple Mode)...")
    executor.start_polling(dp, skip_updates=True) 