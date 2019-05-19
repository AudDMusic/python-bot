import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.utils.exceptions import Throttled


class BaseThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    prefix = "antiflood_"

    class MetaUtils:
        throttled = Throttled
        cancel_handler = CancelHandler
        current_handler = current_handler
        sleep = asyncio.sleep
        dispatcher = Dispatcher

    def __init__(self, limit, tg_bot):
        self.rate_limit = limit
        self.bot = tg_bot

        super(BaseThrottlingMiddleware, self).__init__()
