from itertools import starmap
from dataclasses import dataclass

from text_utils import song_fmt, text, html_fmt


@dataclass
class Response:
    status: str

    error = "error"
    success = "success"


@dataclass
class Song:
    artist: str
    title: str
    album: str
    release_date: str
    label: str
    lyrics: dict = None
    underground: bool = False
    timecode: str = None

    @property
    def pretty_text(self):
        return "\n".join(
            [
                f"{song_fmt(key, 'b')}: {html_fmt(val, 'code')}"
                for key, val in vars(self).items()
                if isinstance(val, str)
            ]
        )


@dataclass
class Lyrics:
    lyrics: str
    title: str
    full_title: str
    title_featured: str

    @property
    def pretty_text(self):
        return html_fmt(self.text, "code")

    @property
    def full_text(self):
        return text(self.full_title, self.lyrics.replace("\r", ""))

    @property
    def text(self):
        lines = []
        for line in self.full_text.splitlines():
            if line and line[0].startswith(" "):
                lines.append(line[1:])
            else:
                lines.append(line)
        return "\n".join(lines)


class LyricsList:
    @staticmethod
    def mapped(func, lyrics_list):
        return list(starmap(func, enumerate(lyrics_list)))
