from aiogram import types

from ..bot import AuddBot, Buttons, Text
from misc import disp

onClick = disp.callback_query_handler


def get_message_with_url(call: types.CallbackQuery):
    message = call.message.reply_to_message
    url = None
    if message:
        url = None
        if message.entities:
            if isinstance(message.entities[0], types.MessageEntityType.URL):
                url = message.text

    return message, url


def call_data_startswith(call: types.CallbackQuery, prefix):
    return call.data.startswith(prefix)


isw = call_data_startswith


@onClick(lambda call: call.data in ['get:lyrics', 'close:lyrics'])
async def get_or_close_lyrics(call: types.CallbackQuery):
    message, url = get_message_with_url(call)

    if message:
        markup = Buttons.get_lyrics_buttons(message) if isw(call, 'close') else Buttons.close_lyrics_buttons(message)
        await call.message.edit_text(Text.loading)
        await call.message.edit_text(await AuddBot.get_lyrics(message, url=url), reply_markup=markup)


@onClick(lambda c: isw(c, 'ocached:') or isw(c, 'ccached:'))
async def close_title(call: types.CallbackQuery):
    cached = call.data.split(':')[-1]
    message = call.message

    await call.message.edit_text(Text.loading)

    txt, buttons = \
        await AuddBot.get_lyrics_by_cache_key(message, cached) if isw(call, 'oc')\
        else await AuddBot.get_song_by_cache_key(message, cached)

    await message.edit_text(txt, reply_markup=buttons)
