from .base import BaseThrottlingMiddleware

from aiogram import types


class TextThrottlingMiddleware(BaseThrottlingMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        handler = self.MetaUtils.current_handler.get()

        dispatcher = self.MetaUtils.dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except self.MetaUtils.throttled as t:
            # call throttler
            await self.message_throttled(message, t)

            # raise stop propagation for current callback
            raise self.MetaUtils.cancel_handler()

    async def message_throttled(self, message: types.Message, throttled):
        handler = self.MetaUtils.current_handler.get()
        dispatcher = self.MetaUtils.dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        delta = throttled.rate - throttled.delta + 2
        if throttled.exceeded_count <= 2:
            setattr(self, 'message_to_edit', await message.reply(f'Bot locked for {round(delta, 2)}'))

        await self.MetaUtils.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            # user unlocked
            to_edit = getattr(self, 'message_to_edit')
            if to_edit:
                await to_edit.edit_text('Bot unlocked')
