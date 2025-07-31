import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class SimpleDatabaseManager:
    def __init__(self):
        self.client = None
        self.sheet = None
        self._connect()
    
    def _connect(self):
        """Initialize Google Sheets connection without API"""
        try:
            # Use a simpler approach - direct access
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            
            # Try to use existing credentials or create a simple connection
            try:
                creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
                self.client = gspread.authorize(creds)
            except FileNotFoundError:
                # Fallback: create a simple connection
                logger.info("No creds.json found, using simple connection")
                self.client = None
            
            # For now, we'll use a mock approach
            self.sheet = None
            logger.info("Using simplified database mode")
            
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            # Continue with mock data for testing
            self.sheet = None
    
    def get_all_cars(self):
        """Get all cars from the database (mock data for now)"""
        # Mock data for testing
        mock_cars = [
            {
                'Марка': 'Chevrolet',
                'Модель': 'Tracker',
                'Год': '2023',
                'Цена': '135 млн',
                'Город': 'Ташкент',
                'Ссылка на фото': 'https://i.imgur.com/azLdCKP.jpeg',
                'Ссылка на банк': 'https://example.com/lot',
                'Телефон': '+998907029845',
                'Телеграм': 'user7990',
                'Статус': '✅ Опубликовано'
            },
            {
                'Марка': 'Chevrolet',
                'Модель': 'Cobalt',
                'Год': '2017',
                'Цена': '199 млн',
                'Город': 'Наманган',
                'Ссылка на фото': 'https://i.imgur.com/azLdCKP.jpeg',
                'Ссылка на банк': 'https://example.com/lot',
                'Телефон': '+998909894109',
                'Телеграм': 'user8192',
                'Статус': '✅ Опубликовано'
            },
            {
                'Марка': 'Daewoo',
                'Модель': 'Nexia',
                'Год': '2016',
                'Цена': '240 млн',
                'Город': 'Фергана',
                'Ссылка на фото': 'https://i.imgur.com/azLdCKP.jpeg',
                'Ссылка на банк': 'https://example.com/lot',
                'Телефон': '+998907131593',
                'Телеграм': 'user3923',
                'Статус': '✅ Опубликовано'
            }
        ]
        return mock_cars
    
    def get_cars_by_filters(self, filters):
        """Get cars filtered by criteria"""
        cars = self.get_all_cars()
        filtered_cars = []
        
        for car in cars:
            if self._matches_filters(car, filters):
                filtered_cars.append(car)
        
        return filtered_cars
    
    def _matches_filters(self, car, filters):
        """Check if car matches all filters"""
        try:
            # Brand filter
            if filters.get('brand') and filters['brand'] != 'all':
                if car.get('Марка', '').lower() != filters['brand'].lower():
                    return False
            
            # Model filter
            if filters.get('model') and filters['model'] != 'all':
                if car.get('Модель', '').lower() != filters['model'].lower():
                    return False
            
            # Year filter
            if filters.get('year') and filters['year'] != 'all':
                if str(car.get('Год', '')).strip() != str(filters['year']):
                    return False
            
            # City filter
            if filters.get('city') and filters['city'] != 'all':
                if car.get('Город', '').lower() != filters['city'].lower():
                    return False
            
            # Price filter
            if filters.get('max_price') and filters['max_price'] != 'all':
                try:
                    price_str = str(car.get('Цена', '')).replace('млн', '').replace('сум', '').strip()
                    car_price = int(price_str.replace(' ', ''))
                    if car_price > int(filters['max_price']):
                        return False
                except (ValueError, AttributeError):
                    return False
            
            # Status filter
            if filters.get('status') == 'new':
                if car.get('Статус', '') == '✅ Опубликовано':
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error in filter matching: {e}")
            return False
    
    def add_car(self, car_data):
        """Add a new car to the database (mock for now)"""
        try:
            logger.info(f"Mock: Added new car: {car_data.get('brand')} {car_data.get('model')}")
            return True
        except Exception as e:
            logger.error(f"Error adding car: {e}")
            return False
    
    def update_car_status(self, row_index, status):
        """Update car status (mock for now)"""
        try:
            logger.info(f"Mock: Updated car status to: {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating car status: {e}")
            return False
    
    def get_unpublished_cars(self):
        """Get cars that are ready for publishing (mock for now)"""
        try:
            # Return mock unpublished cars
            mock_unpublished = [
                {
                    'Марка': 'Chevrolet',
                    'Модель': 'Spark',
                    'Год': '2020',
                    'Цена': '172 млн',
                    'Город': 'Андижан',
                    'Ссылка на фото': 'https://i.imgur.com/azLdCKP.jpeg',
                    'Ссылка на банк': 'https://example.com/lot',
                    'Телефон': '+998909157210',
                    'Телеграм': 'user3705',
                    'Статус': 'Готово',
                    'row_index': 2
                }
            ]
            return mock_unpublished
        except Exception as e:
            logger.error(f"Error getting unpublished cars: {e}")
            return []
    
    def get_unique_values(self, column_name):
        """Get unique values from a specific column"""
        try:
            records = self.get_all_cars()
            values = set()
            
            for record in records:
                if record.get(column_name):
                    values.add(record[column_name].strip())
            
            return sorted(list(values))
        except Exception as e:
            logger.error(f"Error getting unique values for {column_name}: {e}")
            return [] 