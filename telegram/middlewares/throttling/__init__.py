def setup_throttling():
    from . import buttons, text
    from misc import bot, disp

    setup_mdl = disp.middleware.setup
    setup_mdl(buttons.CallbackQuery(1, bot))
    setup_mdl(text.TextThrottlingMiddleware(1, bot))
