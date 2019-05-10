from aiogram.contrib.middlewares.logging import LoggingMiddleware

from misc import disp

disp.middleware.setup(LoggingMiddleware(__name__))
