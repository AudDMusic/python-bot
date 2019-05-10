# TODO: as many of functions are somehow duplicated, @`replace them`

import os
from hashlib import blake2b
import logging

from aiogram import types

from additional.audio import Process
from apiaudd.models import LyricsListMapped, Lyrics, Response
from misc import bot, audd, TOKEN

from locales import Text

logger = logging.getLogger(__name__)

base_url = f'https://api.telegram.org/file/bot{TOKEN}/' + '{file_path}'
VIDEO_DESTINATION = 'videos_tmp/'

markup = types.InlineKeyboardMarkup
button = types.InlineKeyboardButton


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


def create_article(n, lyrics: Lyrics):
    return types.InlineQueryResultArticle(
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                '↗️', switch_inline_query=lyrics.full_title)),
        input_message_content=types.InputTextMessageContent(
            message_text=lyrics.pretty_text[:4096]),
        id=f'{n}',
        title=lyrics.title, description=lyrics.full_title)


class Buttons:
    @staticmethod
    def get_copy(func):
        return {
            'callback_data': f'{func}:lyrics',
            'text': f'{func}Lyrics'  # text key
        }

    @staticmethod
    def __class_getitem__(items):
        """
        Nice magic markup creation
        :param items: event, 'close' or 'get', cache key
        :return:
        """
        kwargs = Buttons.get_copy(items[1])
        kwargs['text'] = Text[kwargs['text'], items[0]]

        if len(items) == 3:
            kwargs['callback_data'] = f'{items[1]}:cached:{items[2]}'

        return markup().add(button(**kwargs))


class AuddBot:
    class ByUrl:
        @staticmethod
        async def get(what: str, message: types.Message, url=None):
            """
            Simple get
            :param what: can be song, lyrics
            :param message:
            :param url:
            :return:
            """

            possible_err = 'lyricsError', 'incorrectInput'

            file_path = await get_file_path(message)
            resp, item = Response('error'), None

            if file_path:
                url = base_url.format(file_path=file_path)
                resp, item = await audd.find_lyrics(url, telegram_file_path=file_path)

            elif not url:
                return Text[possible_err[1], message]

            else:
                if what == 'lyrics':
                    resp, item = await audd.find_lyrics(url)

                elif what == 'song':
                    resp, item = await audd.find_base(url)

            if resp.status == resp.success and item:
                return item.pretty_text

            return Text[possible_err[0], message]

        @staticmethod
        async def lyrics(message, url=None):
            return await AuddBot.ByUrl.get('lyrics', message, url)

        @staticmethod
        async def song(message, url=None):
            return await AuddBot.ByUrl.get('song', message, url)

    @staticmethod
    async def find_lyrics_by_entered(iq: types.InlineQuery):
        resp, lyrics_list = await audd.get_lyrics(iq.query)

        if resp.status == resp.success and lyrics_list:
            results = LyricsListMapped.mapped(create_article, lyrics_list)
            await iq.answer(results, cache_time=0)

    @staticmethod
    async def extract_audio_recognize(msg: types.Message):
        # todo rewrite
        possible_err = 'recognizeError', 'incorrectInput'

        ftype = getattr(msg, 'video') or getattr(msg, 'video_note')
        dur = ftype.duration

        file = await bot.download_file_by_id(ftype.file_id, destination=f'{VIDEO_DESTINATION}{msg.date}')

        proccess = Process(file.name, clip_duration=dur//2)

        base64 = await proccess.convert_to_base64()

        hcache = hash_cache(msg)
        resp, song = await audd.find_by_audio(base64, hcache)

        if resp.status == resp.success and song:
            return song.pretty_text, Buttons[msg, 'get', hcache]

        return Text[possible_err[0], msg], None

    class Cached:
        @staticmethod
        async def get(what: str, message: types.Message, cache_key):
            possible_err = 'recognizeError', 'incorrectInput'
            resp, item, action = Response('error'), None, None

            if what == 'song':
                action = 'get'
                resp, item = await audd.get_cached_song(cache_key)

            elif what == 'lyrics':
                action = 'close'
                resp, item = await audd.find_lyrics(cache_key=cache_key)

            if resp.status == resp.success and item:
                return {'text': item.pretty_text, 'reply_markup': Buttons[message, action, cache_key]}

            return {'text': Text[possible_err[0], message], 'reply_markup': None}

        @staticmethod
        async def lyrics(message, cache_key):
            return await AuddBot.Cached.get('lyrics', message, cache_key)

        @staticmethod
        async def song(message, cache_key):
            return await AuddBot.Cached.get('song', message, cache_key)
