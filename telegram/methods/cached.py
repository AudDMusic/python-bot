from aiogram import types

from apiaudd.models import Response
from locales import Text
from ..buttons import Buttons


class Cached:
    def __init__(self, audd_api):
        self.audd = audd_api

    async def get(self, what: str, message: types.Message, cache_key):
        possible_err = 'recognizeError', 'incorrectInput'
        resp, item, action = Response('error'), None, None

        if what == 'song':
            action = 'get'
            resp, item = await self.audd.get_cached_song(cache_key)

        elif what == 'lyrics':
            action = 'close'
            resp, item = await self.audd.find_lyrics(cache_key=cache_key)

        if resp.status == resp.success and item:
            return {'text': item.pretty_text, 'reply_markup': Buttons[message, action, cache_key]}

        return {'text': Text[possible_err[0], message], 'reply_markup': None}

    async def lyrics(self, message, cache_key):
        return await self.get('lyrics', message, cache_key)

    async def song(self, message, cache_key):
        return await self.get('song', message, cache_key)


__all__ = ['Cached']

