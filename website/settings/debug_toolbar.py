from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
