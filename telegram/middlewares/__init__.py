def setup_all():
    from misc import disp

    setup_mdl = disp.middleware.setup

    from .logging import LoggingMiddleware
    setup_mdl(LoggingMiddleware(__name__))

    from .callbackquery import CallbacksAnswererMiddleware
    setup_mdl(CallbacksAnswererMiddleware())

    from .throttling import setup_throttling
    setup_throttling()
