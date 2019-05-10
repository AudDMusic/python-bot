from aiogram import types

from ..bot import AuddBot, Buttons, Text
from misc import disp

onText = disp.message_handler


@onText(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(
        Text['start', message]
    )


@onText(regexp=r'(www|http:|https:)+[^\s]+[\w]')
async def file_by_url(message: types.Message):
    await message.reply(
        await AuddBot.ByUrl.song(message, url=message.text),
        reply_markup=Buttons[message, 'get']
    )
