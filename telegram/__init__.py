def setup():
    from . import listeners
    listeners.setup_all()

    from . import middlewares
    middlewares.setup_all()
