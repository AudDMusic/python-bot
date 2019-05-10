import asyncio

from aiogram import types, filters

from ..bot import AuddBot
from misc import disp

loop = asyncio.get_event_loop()

onText = disp.message_handler
onFile = disp.message_handler(content_types=[types.ContentType.VOICE, types.ContentType.AUDIO])


def a(*coros):
    for coro in coros:
        loop.create_task(coro)


@onText(commands=['start'])
async def cmd_start(message: types.Message):
    lang = message.from_user.language_code[:2] or 'en'

    await message.reply('Hello send me any voice or url to listenable file!')


@onText(filters.Text(startswith='https://'))
async def file_by_url(message: types.Message):
    await message.reply(await AuddBot.recognize_by_url(message, url=message.text),
                        reply_markup=AuddBot.get_lyrics_board())
