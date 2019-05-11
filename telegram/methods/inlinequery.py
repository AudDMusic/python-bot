from aiogram import types
from emoji import emojize

from apiaudd.models import LyricsList, Lyrics
from ..buttons import Markup, Button


def create_article(n, lyrics: Lyrics):
    markup = Markup().add(Button(
        text=emojize(':arrow_upper_right:', True),
        switch_inline_query=lyrics.full_title)
    )

    return types.InlineQueryResultArticle(
        id=str(n),
        reply_markup=markup,
        input_message_content=types.InputTextMessageContent(message_text=lyrics.pretty_text[:4096]),
        title=lyrics.title,
        description=lyrics.full_title
    )


class Inline:
    def __init__(self, audd_api):
        self.audd = audd_api

    async def find_lyrics_by_entered(self, iq: types.InlineQuery):
        resp, lyrics_list = await self.audd.get_lyrics(iq.query)

        if resp.status == resp.success and lyrics_list:
            results = LyricsList.mapped(create_article, lyrics_list)
            if results:
                await iq.answer(results, cache_time=0)


__all__ = ['Inline']
