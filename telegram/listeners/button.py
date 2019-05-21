import asyncio

from aiogram import types

from locales import Text
from misc import disp

from ..bot import AudDBot
from ..buttons import Buttons

onClick = disp.callback_query_handler

loop = asyncio.get_event_loop()


def tasker(*coros):
    for coro in coros:
        loop.create_task(coro)


def get_message_with_url(call: types.CallbackQuery, url=None):
    message = call.message.reply_to_message

    if message and message.entities:
        if isinstance(message.entities[0], types.MessageEntityType.URL):
            url = message.text

    return message, url


def call_data_startswith(call: types.CallbackQuery, prefix):
    return call.data.startswith(prefix)


isw = call_data_startswith


@onClick(lambda call: call.data in ["get:lyrics", "close:lyrics"])
async def get_or_close_lyrics(call: types.CallbackQuery):
    message, url = get_message_with_url(call)
    edit = call.message.edit_text
    await call.message.edit_reply_markup()

    if message:
        markup = (
            Buttons[message, "get"]
            if isw(call, "close:")
            else Buttons[message, "close"]
        )
        method = AudDBot.ByUrl.song if isw(call, "close:") else AudDBot.ByUrl.lyrics

        tasker(
            types.ChatActions.typing(),
            edit(await method(message, url, False), reply_markup=markup),
        )


@onClick(lambda c: isw(c, "get:cached:") or isw(c, "close:cached:"))
async def close_title(call: types.CallbackQuery):
    cached = call.data.split(":")[-1]
    edit = call.message.edit_text
    await call.message.edit_reply_markup()

    do_get = AudDBot.Cached.lyrics if isw(call, "get:cached") else AudDBot.Cached.song

    tasker(edit(Text.loading), edit(**(await do_get(call.message, cached))))
