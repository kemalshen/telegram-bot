import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8162554421:AAHFrwOptRMM5oiFCUrkiiQAw2glMvvsZLw")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@zalogautouz")

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "creds.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "ZalogAvtoUz")

# Database Column Names (matching your Google Sheet)
COLUMNS = {
    'BRAND': 'Марка',
    'MODEL': 'Модель', 
    'YEAR': 'Год',
    'PRICE': 'Цена',
    'CITY': 'Город',
    'PHOTO_URL': 'Ссылка на фото',
    'BANK_LINK': 'Ссылка на банк',
    'PHONE': 'Телефон',
    'PUBLISH_DATE': 'Дата публикации',
    'TELEGRAM': 'Телеграм',
    'STATUS': 'Статус'
}

# Post Formatting
POST_TEMPLATE = {
    'emoji_car': '🚗',
    'emoji_location': '📍',
    'emoji_price': '💰',
    'emoji_phone': '📞',
    'emoji_telegram': '📱',
    'emoji_link': '🔗',
    'emoji_year': '📅',
    'emoji_condition': '🔧'
}

# Price ranges for filtering
PRICE_RANGES = [
    (0, 100_000_000, "до 100 млн"),
    (100_000_000, 150_000_000, "100-150 млн"),
    (150_000_000, 200_000_000, "150-200 млн"),
    (200_000_000, 300_000_000, "200-300 млн"),
    (300_000_000, 500_000_000, "300-500 млн"),
    (500_000_000, float('inf'), "от 500 млн")
]

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}