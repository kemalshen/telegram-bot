import pytest
from api.post_formatter import PostFormatter

def test_format_car_post():
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
    post = PostFormatter.format_car_post(car_data)
    assert 'text' in post
    assert 'Chevrolet' in post['text']