try:
    import aiohttp  # noqa: F401
except ImportError:
    raise ImportWarning('Please install extras_require "aio" '
                        'for using this module')

from .abc import *  # noqa: F403
from .authz import *  # noqa: F403
from .client import *  # noqa: F403
from .mixins import *  # noqa: F403
from .openid_connect import *  # noqa: F403
from .realm import *  # noqa: F403
from .uma import *  # noqa: F403
from .well_known import *  # noqa: F403
from .. import admin

__all__ = (
        abc.__all__  # noqa: F405
        + admin.__all__
        + authz.__all__  # noqa: F405
        + client.__all__  # noqa: F405
        + mixins.__all__  # noqa: F405
        + openid_connect.__all__  # noqa: F405
        + realm.__all__  # noqa: F405
        + uma.__all__  # noqa: F405
        + well_known.__all__  # noqa: F405
        + ('admin',)
)
