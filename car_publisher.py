from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from database import DatabaseManager
from post_formatter import PostFormatter
from config import COLUMNS

logger = logging.getLogger(__name__)

class CarPublishingStates(StatesGroup):
    waiting_for_brand = State()
    waiting_for_model = State()
    waiting_for_year = State()
    waiting_for_price = State()
    waiting_for_city = State()
    waiting_for_photo = State()
    waiting_for_phone = State()
    waiting_for_telegram = State()
    waiting_for_bank_link = State()
    confirmation = State()

class CarPublisher:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DatabaseManager):
        self.bot = bot
        self.dp = dp
        self.db = db
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all publishing handlers"""
        self.dp.register_message_handler(self.start_publishing, commands=['publish'])
        self.dp.register_message_handler(self.handle_brand, state=CarPublishingStates.waiting_for_brand)
        self.dp.register_message_handler(self.handle_model, state=CarPublishingStates.waiting_for_model)
        self.dp.register_message_handler(self.handle_year, state=CarPublishingStates.waiting_for_year)
        self.dp.register_message_handler(self.handle_price, state=CarPublishingStates.waiting_for_price)
        self.dp.register_message_handler(self.handle_city, state=CarPublishingStates.waiting_for_city)
        self.dp.register_message_handler(self.handle_photo, state=CarPublishingStates.waiting_for_photo)
        self.dp.register_message_handler(self.handle_phone, state=CarPublishingStates.waiting_for_phone)
        self.dp.register_message_handler(self.handle_telegram, state=CarPublishingStates.waiting_for_telegram)
        self.dp.register_message_handler(self.handle_bank_link, state=CarPublishingStates.waiting_for_bank_link)
        self.dp.register_message_handler(self.handle_confirmation, state=CarPublishingStates.confirmation)
        self.dp.register_callback_query_handler(self.confirm_car, lambda c: c.data.startswith('confirm_'))
        self.dp.register_callback_query_handler(self.cancel_publishing, lambda c: c.data == 'cancel_publishing')
    
    async def start_publishing(self, message: types.Message):
        """Start the car publishing process"""
        await message.reply(
            "🚗 <b>Добавление нового автомобиля</b>\n\n"
            "Я помогу вам добавить автомобиль в базу данных.\n"
            "Давайте начнем с марки автомобиля.\n\n"
            "Введите марку автомобиля (например: Chevrolet, Daewoo):",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_brand.set()
    
    async def handle_brand(self, message: types.Message, state: FSMContext):
        """Handle brand input"""
        brand = message.text.strip()
        if len(brand) < 2:
            await message.reply("❌ Марка должна содержать минимум 2 символа. Попробуйте еще раз:")
            return
        
        await state.update_data(brand=brand)
        
        # Get existing models for this brand
        existing_models = self.db.get_unique_values(COLUMNS['MODEL'])
        brand_models = [model for model in existing_models if brand.lower() in model.lower()]
        
        if brand_models:
            kb = InlineKeyboardMarkup(row_width=2)
            for model in brand_models[:6]:  # Limit to 6 buttons
                kb.insert(InlineKeyboardButton(model, callback_data=f"model_{model}"))
            kb.add(InlineKeyboardButton("Другая модель", callback_data="model_other"))
            
            await message.reply(
                f"📝 <b>Марка:</b> {brand}\n\n"
                f"Выберите модель или введите новую:",
                reply_markup=kb,
                parse_mode="HTML"
            )
        else:
            await message.reply(
                f"📝 <b>Марка:</b> {brand}\n\n"
                "Введите модель автомобиля:",
                parse_mode="HTML"
            )
        
        await CarPublishingStates.waiting_for_model.set()
    
    async def handle_model(self, message: types.Message, state: FSMContext):
        """Handle model input"""
        model = message.text.strip()
        if len(model) < 2:
            await message.reply("❌ Модель должна содержать минимум 2 символа. Попробуйте еще раз:")
            return
        
        await state.update_data(model=model)
        data = await state.get_data()
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {model}\n\n"
            "Введите год выпуска автомобиля:",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_year.set()
    
    async def handle_year(self, message: types.Message, state: FSMContext):
        """Handle year input"""
        year = message.text.strip()
        try:
            year_int = int(year)
            if year_int < 1900 or year_int > 2024:
                await message.reply("❌ Год должен быть между 1900 и 2024. Попробуйте еще раз:")
                return
        except ValueError:
            await message.reply("❌ Введите корректный год (например: 2020):")
            return
        
        await state.update_data(year=year)
        data = await state.get_data()
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {data['model']}\n"
            f"📝 <b>Год:</b> {year}\n\n"
            "Введите цену автомобиля (например: 150 млн):",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_price.set()
    
    async def handle_price(self, message: types.Message, state: FSMContext):
        """Handle price input"""
        price = message.text.strip()
        if not price:
            await message.reply("❌ Введите цену автомобиля:")
            return
        
        await state.update_data(price=price)
        data = await state.get_data()
        
        # Get existing cities
        cities = self.db.get_unique_values(COLUMNS['CITY'])
        
        kb = InlineKeyboardMarkup(row_width=2)
        for city in cities[:6]:  # Limit to 6 buttons
            kb.insert(InlineKeyboardButton(city, callback_data=f"city_{city}"))
        kb.add(InlineKeyboardButton("Другой город", callback_data="city_other"))
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {data['model']}\n"
            f"📝 <b>Год:</b> {data['year']}\n"
            f"📝 <b>Цена:</b> {price}\n\n"
            f"Выберите город или введите новый:",
            reply_markup=kb,
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_city.set()
    
    async def handle_city(self, message: types.Message, state: FSMContext):
        """Handle city input"""
        city = message.text.strip()
        if len(city) < 2:
            await message.reply("❌ Город должен содержать минимум 2 символа. Попробуйте еще раз:")
            return
        
        await state.update_data(city=city)
        data = await state.get_data()
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {data['model']}\n"
            f"📝 <b>Год:</b> {data['year']}\n"
            f"📝 <b>Цена:</b> {data['price']}\n"
            f"📝 <b>Город:</b> {city}\n\n"
            "Отправьте ссылку на фото автомобиля:",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_photo.set()
    
    async def handle_photo(self, message: types.Message, state: FSMContext):
        """Handle photo URL input"""
        photo_url = message.text.strip()
        if not photo_url.startswith(('http://', 'https://')):
            await message.reply("❌ Введите корректную ссылку на фото (начинающуюся с http:// или https://):")
            return
        
        await state.update_data(photo_url=photo_url)
        data = await state.get_data()
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {data['model']}\n"
            f"📝 <b>Год:</b> {data['year']}\n"
            f"📝 <b>Цена:</b> {data['price']}\n"
            f"📝 <b>Город:</b> {data['city']}\n"
            f"📝 <b>Фото:</b> ✅\n\n"
            "Введите номер телефона для связи:",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_phone.set()
    
    async def handle_phone(self, message: types.Message, state: FSMContext):
        """Handle phone input"""
        phone = message.text.strip()
        if not phone.startswith('+998'):
            await message.reply("❌ Введите номер телефона в формате +998XXXXXXXXX:")
            return
        
        await state.update_data(phone=phone)
        data = await state.get_data()
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {data['model']}\n"
            f"📝 <b>Год:</b> {data['year']}\n"
            f"📝 <b>Цена:</b> {data['price']}\n"
            f"📝 <b>Город:</b> {data['city']}\n"
            f"📝 <b>Телефон:</b> {phone}\n\n"
            "Введите Telegram username (без @):",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_telegram.set()
    
    async def handle_telegram(self, message: types.Message, state: FSMContext):
        """Handle Telegram username input"""
        telegram = message.text.strip().lstrip('@')
        if not telegram:
            await message.reply("❌ Введите Telegram username:")
            return
        
        await state.update_data(telegram=telegram)
        data = await state.get_data()
        
        await message.reply(
            f"📝 <b>Марка:</b> {data['brand']}\n"
            f"📝 <b>Модель:</b> {data['model']}\n"
            f"📝 <b>Год:</b> {data['year']}\n"
            f"📝 <b>Цена:</b> {data['price']}\n"
            f"📝 <b>Город:</b> {data['city']}\n"
            f"📝 <b>Телефон:</b> {data['phone']}\n"
            f"📝 <b>Telegram:</b> @{telegram}\n\n"
            "Введите ссылку на банк (или отправьте '-' если нет):",
            parse_mode="HTML"
        )
        await CarPublishingStates.waiting_for_bank_link.set()
    
    async def handle_bank_link(self, message: types.Message, state: FSMContext):
        """Handle bank link input"""
        bank_link = message.text.strip()
        if bank_link == '-':
            bank_link = ''
        elif bank_link and not bank_link.startswith(('http://', 'https://')):
            await message.reply("❌ Введите корректную ссылку (начинающуюся с http:// или https://) или отправьте '-':")
            return
        
        await state.update_data(bank_link=bank_link)
        data = await state.get_data()
        
        # Show confirmation
        confirmation_text = (
            f"📋 <b>Проверьте данные автомобиля:</b>\n\n"
            f"🚗 <b>Марка:</b> {data['brand']}\n"
            f"🚗 <b>Модель:</b> {data['model']}\n"
            f"📅 <b>Год:</b> {data['year']}\n"
            f"💰 <b>Цена:</b> {data['price']}\n"
            f"📍 <b>Город:</b> {data['city']}\n"
            f"📞 <b>Телефон:</b> {data['phone']}\n"
            f"📱 <b>Telegram:</b> @{data['telegram']}\n"
        )
        
        if bank_link:
            confirmation_text += f"🔗 <b>Ссылка на банк:</b> {bank_link}\n"
        
        confirmation_text += "\nВсе данные корректны?"
        
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("✅ Подтвердить", callback_data="confirm_yes"),
            InlineKeyboardButton("❌ Отменить", callback_data="cancel_publishing")
        )
        
        await message.reply(confirmation_text, reply_markup=kb, parse_mode="HTML")
        await CarPublishingStates.confirmation.set()
    
    async def confirm_car(self, callback_query: types.CallbackQuery, state: FSMContext):
        """Handle car confirmation"""
        if callback_query.data == "confirm_yes":
            data = await state.get_data()
            
            # Add car to database
            success = self.db.add_car(data)
            
            if success:
                await callback_query.message.edit_text(
                    "✅ <b>Автомобиль успешно добавлен в базу данных!</b>\n\n"
                    "Автомобиль будет опубликован в канале в ближайшее время.",
                    parse_mode="HTML"
                )
            else:
                await callback_query.message.edit_text(
                    "❌ <b>Ошибка при добавлении автомобиля</b>\n\n"
                    "Попробуйте еще раз или обратитесь к администратору.",
                    parse_mode="HTML"
                )
        else:
            await callback_query.message.edit_text(
                "❌ <b>Добавление автомобиля отменено</b>",
                parse_mode="HTML"
            )
        
        await state.finish()
    
    async def cancel_publishing(self, callback_query: types.CallbackQuery, state: FSMContext):
        """Cancel the publishing process"""
        await callback_query.message.edit_text(
            "❌ <b>Добавление автомобиля отменено</b>",
            parse_mode="HTML"
        )
        await state.finish() 