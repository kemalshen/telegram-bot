from pyrogram import Client, filters

api_id = 25797642  # ← твой api_id
api_hash = "4541de2815bcf6cc49902eb48d591772"  # ← твой api_hash
target_channel = "@zalogautouz"  # ← канал-приёмник

app = Client("forward_session", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat("kapital_auto_trade"))
async def forward_message(client, message):
    await message.copy(chat_id=target_channel)

app.run()
