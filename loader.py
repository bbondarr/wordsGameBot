import logging

from aiogram import Bot, Dispatcher, executor

from wordz import Wordz
from config import BOT_API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and the game
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
game = Wordz()