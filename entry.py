import os
import asyncio
import logging

from telegram import setup
from misc import disp

logging.basicConfig(level=int(os.environ.get("LOG_LEVEL", 40)))

loop = asyncio.get_event_loop()


async def polling():
    await disp.skip_updates()
    await disp.start_polling()


def run_bot():
    logger = logging.getLogger(__name__)
    setup()

    try:
        logger.info(f"AudDBot is getting UP")
        loop.run_until_complete(polling())
    except KeyboardInterrupt:
        loop.close()
        exit(1)
