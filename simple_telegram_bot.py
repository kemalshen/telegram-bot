import requests
import json
import time
import logging
from typing import Dict, Any, Optional
from config import BOT_TOKEN, CHANNEL_USERNAME, LOGGING_CONFIG
from simple_database import SimpleDatabaseManager
from post_formatter import PostFormatter

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

class SimpleTelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.db = SimpleDatabaseManager()
        self.offset = 0
        self.session = requests.Session()
    
    def test_connection(self) -> bool:
        """Test bot connection"""
        try:
            url = f"{self.base_url}/getMe"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok"):
                bot_info = data["result"]
                logger.info(f"✅ Bot connected: @{bot_info['username']}")
                return True
            else:
                logger.error(f"❌ Bot connection failed: {data}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = "HTML") -> bool:
        """Send a message to a chat"""
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def send_photo(self, chat_id: str, photo_url: str, caption: str, 
                   reply_markup: Optional[Dict] = None, parse_mode: str = "HTML") -> bool:
        """Send a photo with caption to a chat"""
        url = f"{self.base_url}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            return False
    
    def get_updates(self) -> list:
        """Get updates from Telegram with better error handling"""
        url = f"{self.base_url}/getUpdates"
        params = {
            "offset": self.offset,
            "timeout": 10,  # Reduced timeout
            "limit": 100
        }
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok") and data.get("result"):
                updates = data["result"]
                if updates:
                    self.offset = updates[-1]["update_id"] + 1
                return updates
            return []
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                logger.warning("⚠️  Conflict detected - another bot instance may be running")
                # Reset offset to avoid conflicts
                self.offset = 0
                return []
            else:
                logger.error(f"HTTP Error getting updates: {e}")
                return []
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming message"""
        if "text" not in message:
            return
        
        text = message["text"]
        chat_id = message["chat"]["id"]
        
        logger.info(f"📨 Received message: {text[:50]}... from {chat_id}")
        
        if text.startswith("/start"):
            self.handle_start(chat_id)
        elif text.startswith("/help"):
            self.handle_help(chat_id)
        elif text.startswith("/stats"):
            self.handle_stats(chat_id)
        elif text.startswith("/find"):
            self.handle_find(chat_id)
        elif text.startswith("/publish"):
            self.handle_publish(chat_id)
        else:
            self.send_message(chat_id, "Неизвестная команда. Используйте /help для справки.")
    
    def handle_start(self, chat_id: str) -> None:
        """Handle /start command"""
        welcome_text = (
            "🚗 <b>Добро пожаловать в ZalogAvtoUz Bot!</b>\n\n"
            "Я помогу вам найти и опубликовать залоговые автомобили.\n\n"
            "<b>Доступные команды:</b>\n"
            "🔍 /find — найти автомобили по фильтрам\n"
            "📝 /publish — добавить новый автомобиль\n"
            "📊 /stats — статистика базы данных\n"
            "📋 /help — справка по командам"
        )
        self.send_message(chat_id, welcome_text)
    
    def handle_help(self, chat_id: str) -> None:
        """Handle /help command"""
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
        self.send_message(chat_id, help_text)
    
    def handle_stats(self, chat_id: str) -> None:
        """Handle /stats command"""
        try:
            cars = self.db.get_all_cars()
            brands = self.db.get_unique_values('Марка')
            cities = self.db.get_unique_values('Город')
            
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
            
            self.send_message(chat_id, stats_text)
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            self.send_message(chat_id, "❌ Ошибка при получении статистики")
    
    def handle_find(self, chat_id: str) -> None:
        """Handle /find command"""
        cars = self.db.get_all_cars()
        
        if not cars:
            self.send_message(chat_id, "❌ В базе данных нет автомобилей.")
            return
        
        # Show first few cars as example
        result_text = f"🔍 <b>Найдено автомобилей:</b> {len(cars)}\n\n"
        
        for i, car in enumerate(cars[:5], 1):
            brand = car.get('Марка', '')
            model = car.get('Модель', '')
            year = car.get('Год', '')
            price = car.get('Цена', '')
            city = car.get('Город', '')
            
            result_text += f"{i}. 🚗 <b>{brand} {model}</b>\n"
            result_text += f"   📅 {year} | 📍 {city}\n"
            result_text += f"   💰 {price}\n\n"
        
        if len(cars) > 5:
            result_text += f"... и еще {len(cars) - 5} автомобилей"
        
        self.send_message(chat_id, result_text)
    
    def handle_publish(self, chat_id: str) -> None:
        """Handle /publish command"""
        self.send_message(
            chat_id, 
            "📝 <b>Добавление автомобиля</b>\n\n"
            "Эта функция будет доступна после подключения к Google Sheets.\n"
            "Пока что используйте команду /find для поиска автомобилей."
        )
    
    def run(self) -> None:
        """Main bot loop with improved error handling"""
        logger.info("Starting Simple Telegram Bot...")
        
        # Test connection first
        if not self.test_connection():
            logger.error("❌ Failed to connect to Telegram. Check your bot token.")
            return
        
        logger.info("✅ Bot is running! Send /start to test.")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    if "message" in update:
                        self.handle_message(update["message"])
                
                time.sleep(2)  # Increased delay between requests
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(5)  # Wait before retrying

def main():
    """Main function"""
    bot = SimpleTelegramBot(BOT_TOKEN)
    bot.run()

if __name__ == "__main__":
    main() 