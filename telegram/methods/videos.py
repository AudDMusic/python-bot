import os
from hashlib import blake2b

from aiogram import types

from additional.audio import Process
from locales import Text
from ..buttons import Buttons

VIDEO_DESTINATION = "videos_tmp/"


if not os.path.exists(VIDEO_DESTINATION):
    os.mkdir(VIDEO_DESTINATION)


def hash_cache(event: types.Message):
    """
    Just read func's name
    :param event:
    :return:
    """
    return blake2b(
        f"{event.message_id}:{event.from_user.id}:{event.chat.id}".encode(),
        digest_size=25,
    ).hexdigest()


class Video:
    def __init__(self, audd_api, bot):
        self.audd = audd_api
        self.bot = bot

    async def extract_audio_recognize(self, msg: types.Message):
        possible_err = "recognizeError", "incorrectInput"

        ftype = getattr(msg, "video") or getattr(msg, "video_note")
        dur = ftype.duration

        file = await self.bot.download_file_by_id(
            ftype.file_id, destination=f"{VIDEO_DESTINATION}{msg.date}"
        )

        process = Process(file.name, clip_duration=dur // 2)
        base64 = await process.convert_to_base64()
        h_cache = hash_cache(msg)
        resp, song = await self.audd.find_by_audio(base64, h_cache)

        if resp.status == resp.success and song:
            return song.pretty_text, Buttons[msg, "get", h_cache]

        return Text[possible_err[0], msg], None


__all__ = ["Video"]
