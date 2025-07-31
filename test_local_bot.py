#!/usr/bin/env python3
"""
Final test to verify bot works locally
"""

def test_bot_components():
    """Test all bot components work together"""
    try:
        from simple_telegram_bot import SimpleTelegramBot
        from config import BOT_TOKEN
        
        # Create bot instance
        bot = SimpleTelegramBot(BOT_TOKEN)
        print("✅ Bot instance created successfully")
        
        # Test connection
        if bot.test_connection():
            print("✅ Bot connection test passed")
        else:
            print("❌ Bot connection test failed")
            return False
        
        # Test database integration
        cars = bot.db.get_all_cars()
        print(f"✅ Database integration: {len(cars)} cars loaded")
        
        # Test post formatter
        if cars:
            from post_formatter import PostFormatter
            car = cars[0]
            post_data = PostFormatter.format_car_post(car)
            print(f"✅ Post formatter: Created post with {len(post_data['text'])} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Bot components test failed: {e}")
        return False

def test_telegram_api():
    """Test Telegram API access"""
    try:
        import requests
        from config import BOT_TOKEN
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data["result"]
                print(f"✅ Telegram API: Bot @{bot_info['username']} is accessible")
                return True
            else:
                print(f"❌ Telegram API: {data}")
                return False
        else:
            print(f"❌ Telegram API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🎯 FINAL BOT TEST")
    print("=" * 50)
    
    # Test 1: Telegram API
    print("\n🔍 Testing: Telegram API Access")
    api_ok = test_telegram_api()
    
    # Test 2: Bot Components
    print("\n🔍 Testing: Bot Components")
    components_ok = test_bot_components()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    
    if api_ok and components_ok:
        print("🎉 SUCCESS! Bot is ready to use!")
        print("\n📋 NEXT STEPS:")
        print("1. Send /start to your bot on Telegram")
        print("2. Test commands: /help, /find, /stats")
        print("3. Add creds.json for Google Sheets integration")
        print("4. Deploy to hosting platform")
    else:
        print("⚠️  Some tests failed - check the errors above")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 