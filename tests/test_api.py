import pytest
from api.api import SimpleTelegramBot
from api.config import BOT_TOKEN

def test_bot_connection():
    bot = SimpleTelegramBot(BOT_TOKEN)
    assert bot.test_connection() is True

def test_handle_start(monkeypatch):
    bot = SimpleTelegramBot(BOT_TOKEN)
    called = {}
    def fake_send_message(chat_id, text, parse_mode="HTML"):
        called['sent'] = (chat_id, text)
        return True
    monkeypatch.setattr(bot, 'send_message', fake_send_message)
    bot.handle_start(12345)
    assert 'sent' in called