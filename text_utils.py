from html import escape

from emoji import emojize


EMOJI_ANNOTATIONS = {
    'title': emojize(':bookmark:', True),
    'artist': emojize(':woman_singer:', True),
    'album': emojize(':bookmark_tabs:', True),
    'release_date': emojize(':spiral_calendar_pad:', True),
    'label': emojize(':star:', True)
}


def decode(s: str, _escape: bool = True):
    if _escape:
        return str(escape(s)).encode().decode()
    return str(s).encode().decode()


html_escape = escape


def html_fmt(s: str, fmt='b', use_escape: bool = True):
    if s.lower() in EMOJI_ANNOTATIONS:
        s = f'{EMOJI_ANNOTATIONS[s.lower()]} {s.capitalize()}'

    decoded = decode(s.replace("\r", "").replace("\t", " "), False)
    _decor = html_escape if use_escape else lambda *args, **kwargs: args[0]
    return f'<{fmt}>{_decor(decoded, quote=False).replace("_", " ")}</{fmt}>'


def text(*args, sep='\n'):
    return sep.join(map(str, args))
