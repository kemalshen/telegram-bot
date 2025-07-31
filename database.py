import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from datetime import datetime
from config import GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEET_NAME, COLUMNS

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.sheet = None
        self._connect()
    
    def _connect(self):
        """Initialize Google Sheets connection"""
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                GOOGLE_SHEETS_CREDENTIALS_FILE, scope
            )
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open(GOOGLE_SHEET_NAME).sheet1
            logger.info("Successfully connected to Google Sheets")
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            raise
    
    def get_all_cars(self):
        """Get all cars from the database"""
        try:
            records = self.sheet.get_all_records()
            return [record for record in records if record.get(COLUMNS['BRAND'])]
        except Exception as e:
            logger.error(f"Error getting cars: {e}")
            return []
    
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
                if car.get(COLUMNS['BRAND'], '').lower() != filters['brand'].lower():
                    return False
            
            # Model filter
            if filters.get('model') and filters['model'] != 'all':
                if car.get(COLUMNS['MODEL'], '').lower() != filters['model'].lower():
                    return False
            
            # Year filter
            if filters.get('year') and filters['year'] != 'all':
                if str(car.get(COLUMNS['YEAR'], '')).strip() != str(filters['year']):
                    return False
            
            # City filter
            if filters.get('city') and filters['city'] != 'all':
                if car.get(COLUMNS['CITY'], '').lower() != filters['city'].lower():
                    return False
            
            # Price filter
            if filters.get('max_price') and filters['max_price'] != 'all':
                try:
                    price_str = str(car.get(COLUMNS['PRICE'], '')).replace('млн', '').replace('сум', '').strip()
                    car_price = int(price_str.replace(' ', ''))
                    if car_price > int(filters['max_price']):
                        return False
                except (ValueError, AttributeError):
                    return False
            
            # Status filter
            if filters.get('status') == 'new':
                if car.get(COLUMNS['STATUS'], '') == '✅ Опубликовано':
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error in filter matching: {e}")
            return False
    
    def add_car(self, car_data):
        """Add a new car to the database"""
        try:
            # Prepare row data
            row_data = [
                car_data.get('brand', ''),
                car_data.get('model', ''),
                car_data.get('year', ''),
                car_data.get('price', ''),
                car_data.get('city', ''),
                car_data.get('photo_url', ''),
                car_data.get('bank_link', ''),
                car_data.get('phone', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                car_data.get('telegram', ''),
                'Готово'  # Status: ready for publishing
            ]
            
            self.sheet.append_row(row_data)
            logger.info(f"Added new car: {car_data.get('brand')} {car_data.get('model')}")
            return True
        except Exception as e:
            logger.error(f"Error adding car: {e}")
            return False
    
    def update_car_status(self, row_index, status):
        """Update car status (e.g., mark as published)"""
        try:
            # Find the status column (column K)
            status_col = 11  # Column K
            self.sheet.update_cell(row_index, status_col, status)
            logger.info(f"Updated car status to: {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating car status: {e}")
            return False
    
    def get_unpublished_cars(self):
        """Get cars that are ready for publishing"""
        try:
            records = self.sheet.get_all_records()
            unpublished = []
            
            for i, record in enumerate(records, start=2):  # Start from row 2 (skip header)
                if record.get(COLUMNS['STATUS']) == 'Готово':
                    record['row_index'] = i
                    unpublished.append(record)
            
            return unpublished
        except Exception as e:
            logger.error(f"Error getting unpublished cars: {e}")
            return []
    
    def get_unique_values(self, column_name):
        """Get unique values from a specific column"""
        try:
            records = self.sheet.get_all_records()
            values = set()
            
            for record in records:
                if record.get(column_name):
                    values.add(record[column_name].strip())
            
            return sorted(list(values))
        except Exception as e:
            logger.error(f"Error getting unique values for {column_name}: {e}")
            return [] 