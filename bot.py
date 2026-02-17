import asyncio
import sys

# Fix for Python 3.14+ asyncio event loop issue
if sys.version_info >= (3, 10):
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from config import *
from handlers import anime_handler, movie_handler, admin_handler

app = Client(
    "poster_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

anime_handler.register(app)
movie_handler.register(app)
admin_handler.register(app)

print("Bot is running...")
app.run()

