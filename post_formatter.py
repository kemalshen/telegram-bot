from config import COLUMNS, POST_TEMPLATE
import re

class PostFormatter:
    @staticmethod
    def format_car_post(car_data):
        """Format car data into a professional-looking post"""
        try:
            # Extract car information
            brand = car_data.get(COLUMNS['BRAND'], '')
            model = car_data.get(COLUMNS['MODEL'], '')
            year = car_data.get(COLUMNS['YEAR'], '')
            price = car_data.get(COLUMNS['PRICE'], '')
            city = car_data.get(COLUMNS['CITY'], '')
            photo_url = car_data.get(COLUMNS['PHOTO_URL'], '')
            bank_link = car_data.get(COLUMNS['BANK_LINK'], '')
            phone = car_data.get(COLUMNS['PHONE'], '')
            telegram = car_data.get(COLUMNS['TELEGRAM'], '')
            
            # Format the post
            post_text = PostFormatter._create_post_text(
                brand, model, year, price, city, phone, telegram, bank_link
            )
            
            return {
                'text': post_text,
                'photo_url': photo_url,
                'buttons': PostFormatter._create_buttons(phone, telegram, bank_link)
            }
        except Exception as e:
            return {
                'text': f"❌ Ошибка форматирования: {str(e)}",
                'photo_url': '',
                'buttons': []
            }
    
    @staticmethod
    def _create_post_text(brand, model, year, price, city, phone, telegram, bank_link):
        """Create the main post text"""
        # Car identification
        car_id = f"#{PostFormatter._generate_car_id(brand, model, year)}"
        full_model = f"{brand} {model}"
        
        # Format price
        formatted_price = PostFormatter._format_price(price)
        
        # Build the post
        post_lines = []
        
        # Header with car ID and model
        post_lines.append(f"{POST_TEMPLATE['emoji_car']} <b>{car_id} - {full_model}</b>")
        post_lines.append("")
        
        # Car specifications
        post_lines.append(f"{POST_TEMPLATE['emoji_year']} <b>Год выпуска:</b> {year}")
        post_lines.append(f"{POST_TEMPLATE['emoji_location']} <b>Город:</b> {city}")
        post_lines.append(f"{POST_TEMPLATE['emoji_price']} <b>Цена:</b> {formatted_price}")
        
        # Contact information
        if phone:
            post_lines.append(f"{POST_TEMPLATE['emoji_phone']} <b>Телефон:</b> {phone}")
        if telegram:
            post_lines.append(f"{POST_TEMPLATE['emoji_telegram']} <b>Telegram:</b> @{telegram.lstrip('@')}")
        
        # Additional information
        post_lines.append("")
        post_lines.append(f"{POST_TEMPLATE['emoji_condition']} <b>Состояние:</b> Проверено специалистами")
        
        # Footer
        post_lines.append("")
        post_lines.append("🚗 <b>Залоговые автомобили от банков</b>")
        post_lines.append("💼 <b>Официальные документы</b>")
        post_lines.append("✅ <b>Гарантия качества</b>")
        
        return "\n".join(post_lines)
    
    @staticmethod
    def _generate_car_id(brand, model, year):
        """Generate a unique car ID"""
        # Simple ID generation - you can make this more sophisticated
        import hashlib
        car_string = f"{brand}{model}{year}".lower().replace(' ', '')
        hash_object = hashlib.md5(car_string.encode())
        return hash_object.hexdigest()[:4].upper()
    
    @staticmethod
    def _format_price(price):
        """Format price for display"""
        if not price:
            return "Цена по запросу"
        
        # Clean up the price string
        price_str = str(price).replace('млn', 'млн').replace('сум', '').strip()
        
        # If it's already formatted, return as is
        if 'млн' in price_str:
            return price_str
        
        # Try to format as millions
        try:
            # Remove spaces and convert to number
            clean_price = price_str.replace(' ', '').replace(',', '')
            price_num = int(clean_price)
            
            if price_num >= 1_000_000:
                return f"{price_num // 1_000_000} млн сум"
            else:
                return f"{price_num:,} сум"
        except (ValueError, AttributeError):
            return price_str
    
    @staticmethod
    def _create_buttons(phone, telegram, bank_link):
        """Create inline keyboard buttons"""
        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
        
        buttons = []
        
        # Bank link button
        if bank_link and bank_link != "https://example.com/lot":
            buttons.append(InlineKeyboardButton(
                f"{POST_TEMPLATE['emoji_link']} Подробнее", 
                url=bank_link
            ))
        
        # Phone button
        if phone and phone.startswith('+'):
            buttons.append(InlineKeyboardButton(
                f"{POST_TEMPLATE['emoji_phone']} Позвонить", 
                url=f"tel:{phone}"
            ))
        
        # Telegram button
        if telegram:
            clean_telegram = telegram.lstrip('@')
            buttons.append(InlineKeyboardButton(
                f"{POST_TEMPLATE['emoji_telegram']} Написать", 
                url=f"https://t.me/{clean_telegram}"
            ))
        
        # Create keyboard markup
        if buttons:
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            return keyboard
        
        return None
    
    @staticmethod
    def format_search_results(cars, filters=None):
        """Format search results for display"""
        if not cars:
            return "❌ По вашему запросу ничего не найдено."
        
        result_text = f"🔍 <b>Найдено {len(cars)} автомобилей</b>\n\n"
        
        for i, car in enumerate(cars[:10], 1):  # Limit to 10 results
            brand = car.get(COLUMNS['BRAND'], '')
            model = car.get(COLUMNS['MODEL'], '')
            year = car.get(COLUMNS['YEAR'], '')
            price = car.get(COLUMNS['PRICE'], '')
            city = car.get(COLUMNS['CITY'], '')
            
            result_text += f"{i}. {POST_TEMPLATE['emoji_car']} <b>{brand} {model}</b>\n"
            result_text += f"   {POST_TEMPLATE['emoji_year']} {year} | {POST_TEMPLATE['emoji_location']} {city}\n"
            result_text += f"   {POST_TEMPLATE['emoji_price']} {price}\n\n"
        
        if len(cars) > 10:
            result_text += f"... и еще {len(cars) - 10} автомобилей"
        
        return result_text 