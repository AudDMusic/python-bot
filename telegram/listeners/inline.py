from aiogram import types

from misc import disp

from ..bot import AudDBot


@disp.inline_handler(lambda iq: len(iq.query) >= 3)  # todo make customizable
async def get_lyrics(iq: types.InlineQuery):
    await AudDBot.Inline.find_lyrics_by_entered(iq)
