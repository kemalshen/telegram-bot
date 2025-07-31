# Deployment Guide / Руководство по развертыванию

## 🚀 Quick Start / Быстрый старт

### 1. Railway Deployment (Recommended / Рекомендуется)

#### Step 1: Prepare Your Repository
1. Push all code to GitHub
2. Make sure you have these files:
   - `main.py`
   - `config.py`
   - `database.py`
   - `post_formatter.py`
   - `car_publisher.py`
   - `requirements.txt`
   - `railway.json`

#### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   ```
   BOT_TOKEN=your_telegram_bot_token
   CHANNEL_USERNAME=@zalogautouz
   GOOGLE_SHEET_NAME=ZalogAvtoUz
   ```
6. Add your `creds.json` file to the project
7. Deploy!

### 2. Render Deployment

#### Step 1: Create Render Account
1. Go to [Render.com](https://render.com)
2. Sign up with GitHub

#### Step 2: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `zalogautouz-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

#### Step 3: Add Environment Variables
Add these in Render dashboard:
```
BOT_TOKEN=your_telegram_bot_token
CHANNEL_USERNAME=@zalogautouz
GOOGLE_SHEET_NAME=ZalogAvtoUz
```

#### Step 4: Add Google Sheets Credentials
1. In Render dashboard, go to "Environment" tab
2. Add a new environment variable:
   - **Key**: `GOOGLE_SHEETS_CREDENTIALS`
   - **Value**: Copy the entire content of your `creds.json` file

### 3. Heroku Deployment

#### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add environment variables
heroku config:set BOT_TOKEN=your_telegram_bot_token
heroku config:set CHANNEL_USERNAME=@zalogautouz
heroku config:set GOOGLE_SHEET_NAME=ZalogAvtoUz

# Add Google Sheets credentials
heroku config:set GOOGLE_SHEETS_CREDENTIALS="$(cat creds.json)"

# Deploy
git push heroku main
```

## 🔧 Google Sheets Setup / Настройка Google Sheets

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON credentials file

### Step 2: Setup Google Sheet
1. Create a new Google Sheet
2. Name it "ZalogAvtoUz" (or your preferred name)
3. Add these columns in order:
   ```
   A: Марка
   B: Модель
   C: Год
   D: Цена
   E: Город
   F: Ссылка на фото
   G: Ссылка на банк
   H: Телефон
   I: Дата публикации
   J: Телеграм
   K: Статус
   ```

### Step 3: Share Sheet
1. Share your Google Sheet with the service account email
2. Give it "Editor" permissions

## 🤖 Telegram Bot Setup / Настройка Telegram бота

### Step 1: Create Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow instructions to create bot
4. Save the bot token

### Step 2: Add Bot to Channel
1. Add your bot to your target channel
2. Make it an admin with "Post Messages" permission
3. Get the channel username (e.g., @zalogautouz)

## 📋 Environment Variables / Переменные окружения

Create a `.env` file in your project root:

```env
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token_here
CHANNEL_USERNAME=@zalogautouz

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=creds.json
GOOGLE_SHEET_NAME=ZalogAvtoUz

# Optional
LOG_LEVEL=INFO
```

## 🔍 Troubleshooting / Устранение неполадок

### Common Issues / Частые проблемы:

#### 1. Bot not responding
- Check if BOT_TOKEN is correct
- Verify bot is not blocked
- Check logs for errors

#### 2. Google Sheets connection error
- Verify `creds.json` file is correct
- Check if service account has access to sheet
- Ensure sheet name matches GOOGLE_SHEET_NAME

#### 3. Deployment fails
- Check if all required files are present
- Verify environment variables are set
- Check build logs for Python errors

#### 4. Posts not publishing
- Verify bot is admin in channel
- Check channel username format (@channelname)
- Ensure cars have "Готово" status in sheet

## 📞 Support / Поддержка

If you encounter issues:
1. Check the logs in your hosting platform
2. Verify all environment variables are set
3. Test locally first with `python main.py`
4. Contact support team with error details

## 🎯 Testing / Тестирование

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export BOT_TOKEN=your_token
export CHANNEL_USERNAME=@your_channel

# Run bot
python main.py
```

### Test Commands
1. `/start` - Should show main menu
2. `/help` - Should show help message
3. `/stats` - Should show database statistics
4. `/find` - Should start search process
5. `/publish` - Should start car addition process

## 🚀 Production Checklist / Чек-лист для продакшена

- [ ] Bot token is secure and not in code
- [ ] Google Sheets credentials are properly set
- [ ] Channel permissions are correct
- [ ] Environment variables are configured
- [ ] Database structure matches expected format
- [ ] Error logging is enabled
- [ ] Bot responds to all commands
- [ ] Posts are publishing to channel
- [ ] Search functionality works
- [ ] Car addition workflow works 