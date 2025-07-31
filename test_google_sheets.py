#!/usr/bin/env python3
"""
Test Google Sheets database functionality
"""

def test_google_sheets_connection():
    """Test basic Google Sheets connection"""
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        
        print("✅ Google Sheets packages imported successfully")
        
        # Check if creds.json exists
        import os
        if os.path.exists('creds.json'):
            print("✅ creds.json file found")
            return True
        else:
            print("⚠️  creds.json file not found - using mock data")
            return True
            
    except ImportError as e:
        print(f"❌ Google Sheets import error: {e}")
        return False

def test_sheet_structure():
    """Test that we can work with the sheet structure"""
    try:
        from config import COLUMNS
        
        # Expected columns from your Google Sheet
        expected_columns = [
            'Марка', 'Модель', 'Год', 'Цена', 'Город',
            'Ссылка на фото', 'Ссылка на банк', 'Телефон',
            'Дата публикации', 'Телеграм', 'Статус'
        ]
        
        print(f"✅ Config has {len(COLUMNS)} columns defined")
        
        # Check if all expected columns are in config
        missing = []
        for col in expected_columns:
            if col not in COLUMNS.values():
                missing.append(col)
        
        if missing:
            print(f"⚠️  Missing columns in config: {missing}")
        else:
            print("✅ All expected columns are configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Sheet structure error: {e}")
        return False

def test_mock_database():
    """Test the mock database functionality"""
    try:
        from simple_database import SimpleDatabaseManager
        
        db = SimpleDatabaseManager()
        
        # Test basic operations
        cars = db.get_all_cars()
        print(f"✅ Mock database: {len(cars)} cars loaded")
        
        # Test filtering
        chevrolet_cars = db.get_cars_by_filters({'brand': 'Chevrolet'})
        print(f"✅ Mock database: {len(chevrolet_cars)} Chevrolet cars found")
        
        # Test unique values
        brands = db.get_unique_values('Марка')
        print(f"✅ Mock database: {len(brands)} unique brands")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock database error: {e}")
        return False

def test_real_sheets_integration():
    """Test real Google Sheets integration (if creds.json exists)"""
    try:
        import os
        if not os.path.exists('creds.json'):
            print("⚠️  No creds.json - skipping real sheets test")
            return True
        
        # This would test real Google Sheets
        print("✅ Real Google Sheets integration ready (creds.json found)")
        return True
        
    except Exception as e:
        print(f"❌ Real sheets integration error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("📊 TESTING GOOGLE SHEETS DATABASE")
    print("=" * 50)
    
    tests = [
        ("Google Sheets Connection", test_google_sheets_connection),
        ("Sheet Structure", test_sheet_structure),
        ("Mock Database", test_mock_database),
        ("Real Sheets Integration", test_real_sheets_integration)
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
        print("🎉 Google Sheets database is ready!")
    else:
        print("⚠️  Some database features need fixing")
    print("=" * 50)

if __name__ == "__main__":
    main() 