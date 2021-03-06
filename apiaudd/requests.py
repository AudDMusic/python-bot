import logging
import typing

from aiohttp import ClientSession

from .models import Song, Lyrics, Response
from .errors import is_ok


logger = logging.getLogger(__name__)

API_URL = "https://api.audd.io"

SONG_GET_ARGS = ["title", "artist", "album", "release_date", "label", "lyrics"]
LYRICS_GET_ARGS = ["lyrics", "title", "full_title", "title_featured"]


class MainRequests:
    def __init__(self, api_token: str, telegram_bypass_url: str):
        """
        Main requests class with audd methods
        :param api_token: AudD api token
        :param telegram_bypass_url:  appspot url to bypass roskomparasha
        """
        self.__token = api_token
        self.url = API_URL
        self.bypass_url = telegram_bypass_url

        self.__session = ClientSession()
        self.get = self.__session.get
        self.post = self.__session.post

        self.__headers = {"api_token": api_token}

    async def find_base(
        self, url, telegram_file_path=None, to_return=""
    ) -> typing.Tuple[Response, Song]:
        """
        AudD-recognize method
        :param url: pass file url
        :param telegram_file_path: pass file telegram-url
        :param to_return: return param
        :return: response, song
        """
        url = (
            self.bypass_url % telegram_file_path
            if telegram_file_path and isinstance(url, str) and "telegram" in url
            else url
        )

        params = {"url": url, "return": to_return}
        status, results = await self._base_get(params)
        song = None

        if results:
            song = Song(**{arg: results.get(arg) for arg in SONG_GET_ARGS})

        return Response(status), song

    async def find_lyrics(
        self, url=None, telegram_file_path=None, cache_key=None
    ) -> typing.Tuple[Response, Lyrics]:
        """
        Find lyrics of particular song by cached-string or by url
        :param url: path
        :param telegram_file_path:
        :param cache_key:
        :return: response, single-song-lyrics
        """
        if cache_key:
            resp, song = await self.get_cached_song(cache_key, "lyrics")
        else:
            resp, song = await self.find_base(url, telegram_file_path, "lyrics")

        if song and isinstance(song.lyrics, dict):
            return (
                resp,
                Lyrics(**{key: song.lyrics.get(key, "") for key in LYRICS_GET_ARGS}),
            )

        return resp, None

    async def get_lyrics(
        self, excerpt_or_title: str, max_songs=10
    ) -> typing.Tuple[Response, typing.List[Lyrics]]:
        """
        Get list of lyrics for excerpt
        :param excerpt_or_title:
        :param max_songs:
        :return: response, lyrics-list
        """
        url = self.url + "/findLyrics/"

        params = {"q": excerpt_or_title}
        status, results = await self._base_get(params, url=url)
        lyrics = None

        if results:
            lyrics = [
                Lyrics(**{arg: song.get(arg) for arg in LYRICS_GET_ARGS})
                for song in results[:max_songs]
                if isinstance(song, dict)
            ]

        return Response(status), lyrics

    async def get_cached_song(
        self, cache_key, to_return=""
    ) -> typing.Tuple[Response, Song]:
        """
        Recognition of cached file
        :param cache_key: AudD key for cached file
        :param to_return:
        :return: response, song
        """
        params = {"method": "reminisce", "cache": cache_key, "return": to_return}
        status, results = await self._base_get(**params)
        song = None

        if results:
            song = Song(**{arg: results.get(arg) for arg in SONG_GET_ARGS})
        return Response(status), song

    async def _base_get(
        self, params: dict, key="result", url=None
    ) -> typing.Tuple[str, typing.Any]:
        """
        Base get request designed for AudD api
        :param params: query params
        :param key: key from response json that includes data we need as second param default
        :return: if ok returns `str:status` and `any:results`
        """
        async with self.get(
            url or self.url, params=params, headers=self.__headers
        ) as resp:
            json_resp = await resp.json()
            logging.info(resp)
            if is_ok(resp):
                return json_resp.get("status"), json_resp.get(key)

    async def find_by_audio(
        self, base64: bytes, cache: str, to_return=""
    ) -> typing.Tuple[Response, Song]:
        """
        Get song by base64 encoded string
        :param base64: encoded base64 string
        :param cache: cache-key for further use
        :param to_return: return param
        :return: response, song
        """
        params = {"cache": cache, "return": to_return}

        async with self.post(
            self.url,
            params=params,
            headers=self.__headers,
            data={"audio": base64.decode()},
        ) as resp:
            logger.info(await resp.read())

            song = None
            resp_json = await resp.json() or {}
            results = resp_json.get("result")

            if is_ok(resp) and results:
                song = Song(**{arg: results.get(arg) for arg in SONG_GET_ARGS})

            return Response(resp_json.get("status")), song
