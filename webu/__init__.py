import pkg_resources
import sys

if sys.version_info < (3, 5):
    raise EnvironmentError("Python 3.5 or above is required")

from eth_account import Account  # noqa: E402
from webu.main import Webu  # noqa: E402
from webu.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from webu.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from webu.providers.tester import (  # noqa: E402
    TestRPCProvider,
)
from webu.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from webu.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

__version__ = pkg_resources.get_distribution("webu").version

__all__ = [
    "__version__",
    "Webu",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "EthereumTesterProvider",
    "Account",
]
