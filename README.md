# ZalogAvtoUz Telegram Bot

A professional Telegram bot for managing and publishing car listings from banks' confiscated vehicle databases.

## 🚗 Features / Функции

### Core Features / Основные функции:
- **Car Search & Filtering** / Поиск и фильтрация автомобилей
  - Search by brand, model, year, city, and price
  - Advanced filtering system with interactive buttons
  - Real-time results from Google Sheets database

- **Car Publishing System** / Система публикации автомобилей
  - Step-by-step car addition workflow
  - Professional post formatting with emojis and structured layout
  - Automatic channel publishing with contact buttons

- **Database Management** / Управление базой данных
  - Google Sheets integration for data storage
  - Real-time synchronization
  - Status tracking (Ready/Published)

- **Professional Post Formatting** / Профессиональное форматирование постов
  - Beautiful, structured car posts
  - Contact buttons (Phone, Telegram, Bank Link)
  - Car ID generation and professional styling

### Additional Features / Дополнительные функции:
- **Statistics Dashboard** / Панель статистики
  - Total cars count
  - Brands and cities statistics
  - Popular brands ranking

- **Admin Commands** / Административные команды
  - `/publish_all` - Publish all unpublished cars
  - `/stats` - View database statistics
  - `/help` - Get help and commands list

## 🛠️ Installation / Установка

### Prerequisites / Требования:
- Python 3.7+
- Telegram Bot Token
- Google Sheets API credentials
- Google Sheets database

### Setup Steps / Шаги установки:

1. **Clone the repository** / Клонируйте репозиторий:
```bash
git clone <repository-url>
cd telegram-bot
```

2. **Install dependencies** / Установите зависимости:
```bash
pip install -r requirements.txt
```

3. **Configure environment** / Настройте окружение:
Create a `.env` file with:
```env
BOT_TOKEN=your_telegram_bot_token
CHANNEL_USERNAME=@your_channel_username
GOOGLE_SHEETS_CREDENTIALS_FILE=creds.json
GOOGLE_SHEET_NAME=YourSheetName
```

4. **Setup Google Sheets** / Настройте Google Sheets:
   - Create a Google Sheet with the following columns:
     - Марка (Brand)
     - Модель (Model)
     - Год (Year)
     - Цена (Price)
     - Город (City)
     - Ссылка на фото (Photo URL)
     - Ссылка на банк (Bank Link)
     - Телефон (Phone)
     - Дата публикации (Publication Date)
     - Телеграм (Telegram)
     - Статус (Status)

5. **Get Google Sheets credentials** / Получите учетные данные Google Sheets:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Sheets API
   - Create service account credentials
   - Download `creds.json` file
   - Share your Google Sheet with the service account email

## 🚀 Deployment / Развертывание

### Recommended Hosting Platforms / Рекомендуемые платформы хостинга:

#### 1. Railway (Recommended / Рекомендуется)
- Free tier available
- Easy deployment from GitHub
- Automatic environment variable management

#### 2. Render
- Free tier available
- Easy setup with GitHub integration
- Good for Python applications

#### 3. Heroku
- Paid platform
- Reliable and scalable
- Good for production use

### Deployment Steps / Шаги развертывания:

#### Railway Deployment:
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

#### Render Deployment:
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variables

## 📋 Usage / Использование

### Bot Commands / Команды бота:

- `/start` - Main menu and welcome message
- `/find` - Search cars by filters
- `/publish` - Add new car to database
- `/publish_all` - Publish all unpublished cars to channel
- `/stats` - View database statistics
- `/help` - Get help and commands list

### User Workflow / Рабочий процесс пользователя:

1. **Searching Cars** / Поиск автомобилей:
   - Use `/find` command
   - Select brand, model, year, city, and price range
   - View filtered results

2. **Adding Cars** / Добавление автомобилей:
   - Use `/publish` command
   - Follow step-by-step form
   - Enter car details (brand, model, year, price, city, photo, contacts)
   - Confirm and save to database

3. **Publishing to Channel** / Публикация в канал:
   - Use `/publish_all` to publish all unpublished cars
   - Cars are automatically formatted with professional layout
   - Contact buttons are added for easy communication

## 🏗️ Project Structure / Структура проекта

```
telegram-bot/
├── main.py              # Main bot file
├── config.py            # Configuration settings
├── database.py          # Google Sheets database manager
├── post_formatter.py    # Professional post formatting
├── car_publisher.py     # Car publishing workflow
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment variables (create this)
└── creds.json         # Google Sheets credentials (add this)
```

## 🔧 Configuration / Конфигурация

### Environment Variables / Переменные окружения:

- `BOT_TOKEN` - Your Telegram bot token
- `CHANNEL_USERNAME` - Target channel username (e.g., @zalogautouz)
- `GOOGLE_SHEETS_CREDENTIALS_FILE` - Path to Google Sheets credentials file
- `GOOGLE_SHEET_NAME` - Name of your Google Sheet

### Google Sheets Structure / Структура Google Sheets:

The bot expects a Google Sheet with these columns:
- A: Марка (Brand)
- B: Модель (Model)
- C: Год (Year)
- D: Цена (Price)
- E: Город (City)
- F: Ссылка на фото (Photo URL)
- G: Ссылка на банк (Bank Link)
- H: Телефон (Phone)
- I: Дата публикации (Publication Date)
- J: Телеграм (Telegram)
- K: Статус (Status)

## 🎯 Features Description / Описание функций

### Car Publishing Workflow / Рабочий процесс публикации автомобилей:
- **Step-by-step form** / Пошаговая форма
- **Data validation** / Валидация данных
- **Professional formatting** / Профессиональное форматирование
- **Automatic database updates** / Автоматическое обновление базы данных

### Search and Filter System / Система поиска и фильтрации:
- **Multi-criteria filtering** / Многофакторная фильтрация
- **Interactive buttons** / Интерактивные кнопки
- **Real-time results** / Результаты в реальном времени
- **User-friendly interface** / Удобный интерфейс

### Professional Post Formatting / Профессиональное форматирование постов:
- **Structured layout** / Структурированный макет
- **Contact buttons** / Кнопки контактов
- **Car ID generation** / Генерация ID автомобиля
- **Professional styling** / Профессиональное оформление

## 🚀 Future Enhancements / Будущие улучшения

### Planned Features / Планируемые функции:
- **Seller Rating System** / Система рейтинга продавцов
- **Feedback Collection** / Сбор отзывов
- **Analytics Dashboard** / Панель аналитики
- **Automated Publishing** / Автоматическая публикация
- **Advanced Filtering** / Расширенная фильтрация
- **Mobile App Integration** / Интеграция с мобильным приложением

## 📞 Support / Поддержка

For technical support or questions, please contact the development team.

Для технической поддержки или вопросов, пожалуйста, обратитесь к команде разработки.

## 📄 License / Лицензия

This project is proprietary software. All rights reserved.

Этот проект является проприетарным программным обеспечением. Все права защищены. 