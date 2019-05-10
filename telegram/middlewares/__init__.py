def setup_all():
    from .throttling import setup_throttling
    setup_throttling()

    from .logging import LoggingMiddleware
    LoggingMiddleware.setup()
