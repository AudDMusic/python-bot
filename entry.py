import asyncio
import logging

from telegram import setup
from misc import disp

loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)


async def polling():
    await disp.skip_updates()
    await disp.start_polling()


def run_bot():
    setup()

    try:
        logger.info(f"AudDBot is getting UP")
        loop.run_until_complete(polling())
    except KeyboardInterrupt:
        loop.close()
        exit(1)
