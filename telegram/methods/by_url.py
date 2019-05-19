from aiogram import types

from apiaudd.models import Response
from locales import Text
from misc import TOKEN

from ..buttons import Buttons

base_url = f"https://api.telegram.org/file/bot{TOKEN}/" + "{file_path}"


async def get_file_path(message: types.Message):
    ftype = message.voice or message.audio
    return (await ftype.get_file()).file_path


class ByUrl:
    def __init__(self, audd_api):
        self.audd = audd_api

    async def get(
        self, what: str, message: types.Message, url=None, return_markup=True
    ):
        """
        Simple get
        :param what: can be song, lyrics
        :param message: replied message
        :param url:
        :param return_markup:
        :return: str: answer
        """
        possible_err = "lyricsError", "incorrectInput", "recognizeError"
        callback_data = "close" if what == "lyrics" else "get"

        file_path = await get_file_path(message)
        resp, item = Response("error"), None

        if file_path:
            url = base_url.format(file_path=file_path)

        if not url:
            return Text[possible_err[1], message], None

        if what == "lyrics":
            resp, item = await self.audd.find_lyrics(url, telegram_file_path=file_path)

        elif what == "song":
            resp, item = await self.audd.find_base(url, telegram_file_path=file_path)

        if resp.status == resp.success:
            if item:
                text, markup = item.pretty_text, Buttons[message, callback_data]
            else:
                text, markup = Text[possible_err[2], message], None
        else:
            text, markup = Text[possible_err[0], message], None

        if return_markup:
            return text, markup
        return text

    async def lyrics(self, message, url=None, return_markup=True):
        """
        Get song lyrics
        :param message:
        :param url:
        :param return_markup:
        :return:
        """
        return await self.get("lyrics", message, url, return_markup)

    async def song(self, message, url=None, return_markup=True):
        """
        Get song
        :param message:
        :param url:
        :param return_markup:
        :return:
        """
        return await self.get("song", message, url, return_markup)


__all__ = ["ByUrl"]
