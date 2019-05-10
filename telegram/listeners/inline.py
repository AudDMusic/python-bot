from aiogram import types

from misc import disp

from ..bot import AuddBot


@disp.inline_handler(lambda iq: len(iq.query) >= 3)
async def get_lyrics(iq: types.InlineQuery):
    await AuddBot.find_lyrics_by_entered(iq)
