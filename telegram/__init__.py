def setup():
    from .listeners import text, file, button, inline
    disp = inline.disp

    setup_mdl = disp.middleware.setup

    from .middlewares.logging import LoggingMiddleware
    setup_mdl(LoggingMiddleware(__name__))

    from .middlewares.callbackquery import CallbacksAnswererMiddleware
    setup_mdl(CallbacksAnswererMiddleware())

    from .middlewares.throttling import setup_throttling
    setup_throttling()
