import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apiaudd.requests import MainRequests

var = os.environ.get

TOKEN = var('BOT_TOKEN')
bot = Bot(TOKEN, parse_mode='html')
disp = Dispatcher(bot, storage=MemoryStorage())

APP_SPOT_URL = f'https://esc-ru.appspot.com/file/bot{TOKEN}/%s?host=api.telegram.org'
audd = MainRequests(var('AUDD_TOKEN'), APP_SPOT_URL)
