from aiogram.contrib.middlewares.logging import LoggingMiddleware

from misc import disp

disp.middleware.setup(LoggingMiddleware(__name__))

"""
Logging middleware is used to log bot-related events
"""
