import asyncio

from aiogram import types

from locales import Text
from misc import disp

from ..bot import AudDBot

loop = asyncio.get_event_loop()

onText = disp.message_handler


def tasker(*coros):
    for coro in coros:
        loop.create_task(coro)


async def fetch_song(message):
    txt, markup = await AudDBot.ByUrl.song(message, url=message.text)
    await message.reply(text=txt, reply_markup=markup)


@onText(regexp=r"(www|http:|https:)+[^\s]+[\w]")
async def file_by_url(message: types.Message):
    tasker(types.ChatActions.typing(), fetch_song(message))


@onText(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply(Text["start", message])
