def load_middleware():
    from . import buttons, text


def setup_throttling():
    from . import buttons, text
    from misc import bot, disp

    setup = disp.middleware.setup
    setup(buttons.CallbackQuery(1, bot))
    setup(text.TextThrottlingMiddleware(1, bot))
