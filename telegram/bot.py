import os
from hashlib import blake2b
import logging

from aiogram import types, exceptions

from additional.audio import Process
from misc import bot, audd

from locales import Text

logger = logging.getLogger(__name__)

base_url = 'https://api.telegram.org/file/bot%s/{file_path}' % getattr(bot, '_BaseBot__token')
VIDEO_DESTINATION = 'videos_tmp/'


if not os.path.exists(VIDEO_DESTINATION):
    os.mkdir(VIDEO_DESTINATION)


def hash_cache(event: types.Message):
    """
    Just read func's name
    :param event:
    :return:
    """
    return blake2b(f'{event.message_id}:{event.from_user.id}:{event.chat.id}'.encode(), digest_size=25).hexdigest()


async def get_file_path(message: types.Message):
    ftype = getattr(message, 'voice') or getattr(message, 'audio')
    return (await ftype.get_file()).file_path


def _get_lyrics_list(iq, lyrics_list, lyrics_attr='pretty_text', default_lyrics_attr='...'):
    return [types.InlineQueryResultArticle(
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('↗️', switch_inline_query=lyrics.full_title)),
        input_message_content=types.InputTextMessageContent(
            message_text=f'{getattr(lyrics, lyrics_attr)[:4096], default_lyrics_attr}'),
        id=f'{n}',
        title=lyrics.title, description=lyrics.full_title)
        for n, lyrics in enumerate(lyrics_list)
    ]


class Buttons:
    @staticmethod
    def close_lyrics_buttons(event, cache=''):
        key = 'close:lyrics'
        if cache:
            key = f'ccached:{cache}'
        return types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(Text['closeLyrics', event], callback_data=key))

    @staticmethod
    def get_lyrics_buttons(event, cache=''):
        key = 'get:lyrics'
        if cache:
            key = f'ocached:{cache}'
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton(text=Text['getLyrics', event], callback_data=key))


class AuddBot:
    @staticmethod
    async def recognize_by_url(message: types.Message, url=None):
        possible_err = 'recognizeError', 'incorrectInput'

        file_path = await get_file_path(message)

        if file_path:
            url = base_url.format(file_path=file_path)
            resp, song = await audd.find_base(url, telegram_file_path=file_path)

        elif not url and not file_path:
            return Text[possible_err[1], message]

        else:
            resp, song = await audd.find_base(url)

        if all([resp.status == resp.success, song]):
            return song.pretty_text

        return Text[possible_err[0], message]

    @staticmethod
    async def get_lyrics(message: types.Message, url=None):
        possible_err = 'lyricsError', 'incorrectInput'

        file_path = await get_file_path(message)

        if file_path:
            url = base_url.format(file_path=file_path)
            resp, lyrics = await audd.find_lyrics(url, telegram_file_path=file_path)

        elif not url and not file_path:
            return Text[possible_err[1], message]

        else:
            resp, lyrics = await audd.find_lyrics(url)

        if all([resp.status == resp.success, lyrics]):
            return lyrics.pretty_text

        return Text[possible_err[0], message]

    @staticmethod
    async def find_lyrics_by_entered(iq: types.InlineQuery):
        resp, lyrics_list = await audd.get_lyrics(iq.query)

        if resp.status == resp.success and lyrics_list:
            results = _get_lyrics_list(iq, lyrics_list)

            try:
                await iq.answer(results, cache_time=0)
            except exceptions.CantParseEntities:
                results = _get_lyrics_list(iq, lyrics_list, 'text')
                await iq.answer(results, cache_time=0)

    @staticmethod
    async def extract_audio_recognize(msg: types.Message):
        possible_err = 'recognizeError', 'incorrectInput'

        ftype = getattr(msg, 'video') or getattr(msg, 'video_note')
        dur = ftype.duration

        file = await bot.download_file_by_id(ftype.file_id, destination=f'{VIDEO_DESTINATION}{msg.date}')

        proccess = Process(file.name, clip_duration=dur//2)

        base64 = await proccess.convert_to_base64(True)

        hcache = hash_cache(msg)
        resp, song = await audd.find_by_audio(base64, hcache)

        if all([resp.status == resp.success, song]):
            return song.pretty_text, Buttons.get_lyrics_buttons(msg, hcache)

        return Text[possible_err[0], msg], None

    @staticmethod
    async def get_song_by_cache_key(msg: types.Message, cache_key):
        possible_err = 'recognizeError', 'incorrectInput'

        resp, song = await audd.get_cached_song(cache_key)

        if all([resp.status == resp.success, song]):
            return song.pretty_text, Buttons.get_lyrics_buttons(msg, cache_key)

        return Text[possible_err[0], msg], None

    @staticmethod
    async def get_lyrics_by_cache_key(msg: types.Message, cache_key):
        possible_err = 'recognizeError', 'incorrectInput'

        resp, lyrics = await audd.find_lyrics(cache_key=cache_key)

        if all([resp.status == resp.success, lyrics]):
            return lyrics.pretty_text, Buttons.close_lyrics_buttons(msg, cache_key)

        return Text[possible_err[0], msg], None
