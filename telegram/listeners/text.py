from aiogram import types

from locales import Text
from misc import disp

from ..bot import AudDBot

onText = disp.message_handler


@onText(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(
        Text['start', message]
    )


@onText(regexp=r'(www|http:|https:)+[^\s]+[\w]')
async def file_by_url(message: types.Message):
    txt, markup = await AudDBot.ByUrl.song(message, url=message.text)

    await message.reply(
        text=txt,
        reply_markup=markup
    )
