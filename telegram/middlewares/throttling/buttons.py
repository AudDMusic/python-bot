from .base import BaseThrottlingMiddleware

from aiogram import types


class CallbackQuery(BaseThrottlingMiddleware):
    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        handler = self.MetaUtils.current_handler.get()

        dispatcher = self.MetaUtils.dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(
                handler, "throttling_key", f"{self.prefix}_{handler.__name__}"
            )
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_call"

        try:
            await dispatcher.throttle(key, rate=limit)
        except self.MetaUtils.throttled as t:
            # call throttler
            await self.call_throttled(call, t)

            # raise stop propagation for current callback
            raise self.MetaUtils.cancel_handler()

    async def call_throttled(self, call: types.CallbackQuery, throttled):
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await call.answer(f"You were banned\nWait {delta}")

        await self.MetaUtils.sleep(delta)
