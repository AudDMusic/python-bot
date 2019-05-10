import os
import hashlib
import logging
import asyncio
import base64

from moviepy.editor import VideoFileClip

logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()

F_TO_DEFAULT = (2, 12)
AUDIOS_DIR = 'audios_tmp'

if not os.path.exists(AUDIOS_DIR):
    os.mkdir(AUDIOS_DIR)


def _2blake2b(s: str):
    return hashlib.blake2b(s.encode(), digest_size=10).hexdigest()


class Process:
    def __init__(self, clip_path: str, audio_path: str = None, clip_duration=F_TO_DEFAULT):
        self.clip_path = clip_path
        self.audio_path = audio_path or f'{AUDIOS_DIR}/{_2blake2b(clip_path)}.mp3'
        self.base64 = None
        self.clip_duration = clip_duration

    def _run(self):
        clip = VideoFileClip(self.clip_path).subclip(1, self.clip_duration)
        clip.audio.write_audiofile(self.audio_path, logger=None)

        with open(self.audio_path, mode="rb") as fp:
            self.base64 = base64.b64encode(fp.read())

    async def convert_to_base64(self, r=None):
        """

        :param r: passing True will erase both clip and audio files saved locally
                  passing float point number will take it as a timeout to delete after r
                  passing anything else won't do anything
        :return:
        """
        await loop.run_in_executor(None, self._run)

        if isinstance(r, float) or r:
            timeout = r
            if isinstance(r, bool):
                timeout = .1

            async def inner_task():
                await asyncio.sleep(timeout)
                for file in [self.clip_path, self.audio_path]:
                    os.remove(file)
            loop.create_task(inner_task())

        return self.base64
