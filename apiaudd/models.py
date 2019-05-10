from dataclasses import dataclass

from text_utils import html_fmt, text


@dataclass
class Response:
    status: str

    error = 'error'
    success = 'success'


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

    parse_mode = 'html'

    @property
    def pretty_text(self):
        return '\n'.join([f"{html_fmt(key.capitalize())}: {html_fmt(val, 'code')}"
                          for key, val in vars(self).items() if isinstance(val, str)])


@dataclass
class Lyrics:
    lyrics: str
    title: str
    full_title: str
    title_featured: str

    @property
    def pretty_text(self):
        return text(html_fmt(self.text, 'code'))

    @property
    def _text(self):
        return text(self.full_title, self.lyrics.replace('\r', ''))

    @property
    def text(self):
        return self._get_nice

    @property
    def _get_nice(self):
        lines = []
        for line in self._text.splitlines():
            if line and line[0].startswith(' '):
                lines.append(line[1:])
            else:
                lines.append(line)
        return '\n'.join(lines)
