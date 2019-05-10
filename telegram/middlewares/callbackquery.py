from aiogram.dispatcher.middlewares import BaseMiddleware

from locales import Text


class CallbacksAnswererMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_callback_query(callback_query, *args):
        await callback_query.answer(Text['ad', callback_query])
