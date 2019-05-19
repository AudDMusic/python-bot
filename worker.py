import logging

from entry import run_bot

logger = logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    logger.info("Started setting everything up...")
    run_bot()
