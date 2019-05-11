from html import escape

from emoji import emojize


EMOJI_ANNOTATIONS = {
    'title': emojize(':bookmark:', True),
    'artist': emojize(':woman_singer:', True),
    'album': emojize(':bookmark_tabs:', True),
    'release_date': emojize(':spiral_calendar_pad:', True),
    'label': emojize(':star:', True)
}


def decode(s: str, use_escape: bool = True):
    if use_escape:
        return str(escape(s)).encode().decode()
    return str(s).encode().decode()


def html_fmt(s: str, fmt='b', use_escape: bool = True):
    decoded = decode(s.replace("\r", "").replace("\t", " "), False)
    decor = escape if use_escape else lambda *args, **kwargs: args[0]
    return f'<{fmt}>{decor(decoded, quote=False).replace("_", " ")}</{fmt}>'


def song_fmt(s: str, fmt='', use_escape: bool = True):
    if s.lower() in EMOJI_ANNOTATIONS:
        s = f'{EMOJI_ANNOTATIONS[s.lower()]} {s.capitalize()}'
    return html_fmt(s, fmt, use_escape)


def text(*args, sep='\n'):
    return sep.join(map(str, args))
