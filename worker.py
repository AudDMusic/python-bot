import logging

from entry import run_bot

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Started setting everything up...")
    run_bot()
