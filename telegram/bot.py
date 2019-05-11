import logging

from .methods import inlinequery, by_url, cached, videos
from misc import bot, audd

logger = logging.getLogger(__name__)


class AudDBot:
    Cached = cached.Cached(audd)
    Inline = inlinequery.Inline(audd)
    ByUrl = by_url.ByUrl(audd)
    Video = videos.Video(audd, bot)
