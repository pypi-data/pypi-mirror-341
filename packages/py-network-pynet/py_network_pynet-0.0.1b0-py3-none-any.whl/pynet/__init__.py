from .better_thread import BetterThread
from .better_process import BetterProcess
from .better_connection import BetterConnection,ConnectionRole

_ = dict([(x.name,x) for x in ConnectionRole])
if 'OFF_' not in _:
    _['OFF_'] = ConnectionRole(0)
locals().update(_)
del _

from .server import ServerConnection,ServerNetworking
from .client import ClientConnection,ClientNetworking

__version__ = '0.0.1.beta.0'
