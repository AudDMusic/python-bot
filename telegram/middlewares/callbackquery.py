from aiogram.dispatcher.middlewares import BaseMiddleware

from locales import Text


class CallbacksAnswererMiddleware(BaseMiddleware):
    """
    Base middleware handler to handle all callback-queries and answer with ad
    """

    @staticmethod
    async def on_pre_process_callback_query(callback_query, *args):
        await callback_query.answer(Text["ad", callback_query])
