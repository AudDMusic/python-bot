import logging

from .base import BaseThrottlingMiddleware

from aiogram import types


logger = logging.getLogger(__name__)


class InlineQuery(BaseThrottlingMiddleware):
    async def on_process_inline_query(self, iq: types.InlineQuery, data: dict):
        handler = self.MetaUtils.current_handler.get()

        dispatcher = self.MetaUtils.dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_iq"

        try:
            await dispatcher.throttle(key, rate=limit)
        except self.MetaUtils.throttled as t:
            # call throttler
            await self.query_throttled(iq, t)

            # raise stop propagation for current callback
            raise self.MetaUtils.cancel_handler()

    async def query_throttled(self, iq: types.InlineQuery, throttled):
        handler = self.MetaUtils.current_handler.get()
        dispatcher = self.MetaUtils.dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_iq"

        delta = throttled.rate - throttled.delta + 2

        if throttled.exceeded_count <= 2:
            # let user pm bot instead of using abusing service from inline_query
            setattr(self, 'iq_to_answer', await iq.answer(
                results=[], cache_time=delta, switch_pm_text=f'You are banned for {round(delta, 2)}',
                switch_pm_parameter='start'))

        await self.MetaUtils.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            # user unlocked
            to_edit = getattr(self, 'iq_to_answer')

            if to_edit:
                try:
                    await to_edit.answer(results=[], cache_time=0, switch_pm_text=f'Unlocked',
                                         switch_pm_parameter='start')
                except Exception as err:
                    # known case when query gets outdated
                    logger.info(err)
