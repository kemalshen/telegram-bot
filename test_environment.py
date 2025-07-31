#!/usr/bin/env python3
"""
Simple test to verify Python environment is working
"""

def hello_world():
    """Simple hello world function"""
    return "Hello, World! Python environment is working! 🐍"

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import requests
        import json
        import logging
        import time
        from typing import Dict, Any, Optional
        print("✅ All basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config import BOT_TOKEN, CHANNEL_USERNAME
        print(f"✅ Config loaded - Bot token: {BOT_TOKEN[:10]}...")
        print(f"✅ Channel: {CHANNEL_USERNAME}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🧪 TESTING PYTHON ENVIRONMENT")
    print("=" * 50)
    
    # Test 1: Basic Python
    print(f"\n1️⃣ Basic Python: {hello_world()}")
    
    # Test 2: Imports
    print(f"\n2️⃣ Package imports: {'✅ PASS' if test_imports() else '❌ FAIL'}")
    
    # Test 3: Config
    print(f"\n3️⃣ Configuration: {'✅ PASS' if test_config() else '❌ FAIL'}")
    
    print("\n" + "=" * 50)
    print("🎉 Environment test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 