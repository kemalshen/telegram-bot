#!/usr/bin/env python3
"""
Test to verify all bot features are implemented
"""

def test_database_features():
    """Test database functionality"""
    try:
        from simple_database import SimpleDatabaseManager
        db = SimpleDatabaseManager()
        
        # Test getting cars
        cars = db.get_all_cars()
        print(f"✅ Database: Found {len(cars)} cars")
        
        # Test getting unique values
        brands = db.get_unique_values('Марка')
        cities = db.get_unique_values('Город')
        print(f"✅ Database: {len(brands)} brands, {len(cities)} cities")
        
        # Test filtering
        filtered = db.get_cars_by_filters({'brand': 'Chevrolet'})
        print(f"✅ Database: Filtered {len(filtered)} Chevrolet cars")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_post_formatter():
    """Test post formatting"""
    try:
        from post_formatter import PostFormatter
        
        # Test car data
        car_data = {
            'Марка': 'Chevrolet',
            'Модель': 'Tracker',
            'Год': '2023',
            'Цена': '135 млн',
            'Город': 'Ташкент',
            'Ссылка на фото': 'https://i.imgur.com/azLdCKP.jpeg',
            'Телефон': '+998907029845',
            'Телеграм': 'user7990'
        }
        
        # Test formatting
        post_data = PostFormatter.format_car_post(car_data)
        print(f"✅ Post formatter: Created post with {len(post_data['text'])} characters")
        
        # Test search results
        cars = [car_data]
        results = PostFormatter.format_search_results(cars)
        print(f"✅ Post formatter: Created search results with {len(results)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Post formatter error: {e}")
        return False

def test_bot_commands():
    """Test bot command handlers"""
    try:
        from simple_telegram_bot import SimpleTelegramBot
        
        # Create bot instance (won't actually connect)
        bot = SimpleTelegramBot("test_token")
        
        # Test that all command handlers exist
        handlers = [
            'handle_start',
            'handle_help', 
            'handle_stats',
            'handle_find',
            'handle_publish'
        ]
        
        for handler in handlers:
            if hasattr(bot, handler):
                print(f"✅ Bot: {handler} handler exists")
            else:
                print(f"❌ Bot: {handler} handler missing")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Bot error: {e}")
        return False

def test_configuration():
    """Test all configuration settings"""
    try:
        from config import BOT_TOKEN, CHANNEL_USERNAME, COLUMNS, POST_TEMPLATE
        
        print(f"✅ Config: Bot token configured")
        print(f"✅ Config: Channel set to {CHANNEL_USERNAME}")
        print(f"✅ Config: {len(COLUMNS)} database columns defined")
        print(f"✅ Config: {len(POST_TEMPLATE)} post template elements")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🤖 TESTING BOT FEATURES")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Database Features", test_database_features),
        ("Post Formatter", test_post_formatter),
        ("Bot Commands", test_bot_commands)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            print(f"✅ {test_name}: PASS")
            passed += 1
        else:
            print(f"❌ {test_name}: FAIL")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 All bot features are working!")
    else:
        print("⚠️  Some features need fixing")
    print("=" * 50)

if __name__ == "__main__":
    main() 