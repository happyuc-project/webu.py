import pytest

from webu import Webu

from .common import (
    HappyUCGoEthModuleTest,
    HappyUCGoNetModuleTest,
    HappyUCGoPersonalModuleTest,
    HappyUCGoTest,
    HappyUCGoVersionModuleTest,
    get_open_port,
)
from .utils import (
    wait_for_http,
)


@pytest.fixture(scope="module")
def rpc_port():
    return get_open_port()


@pytest.fixture(scope="module")
def endpoint_uri(rpc_port):
    return 'http://localhost:{0}'.format(rpc_port)


@pytest.fixture(scope='module')
def ghuc_command_arguments(ghuc_binary, datadir, rpc_port):
    return (
        ghuc_binary,
        '--datadir', str(datadir),
        '--nodiscover',
        '--fakepow',
        '--rpc',
        '--rpcport', rpc_port,
        '--rpcapi', 'db,eth,net,webu,personal,webu',
        '--ipcdisable',
    )


@pytest.fixture(scope="module")
def webu(ghuc_process, endpoint_uri):
    wait_for_http(endpoint_uri)
    _webu = Webu(Webu.HTTPProvider(endpoint_uri))
    return _webu


class TestHappyUCGoTest(HappyUCGoTest):
    pass


class TestHappyUCGoEthModuleTest(HappyUCGoEthModuleTest):
    pass


class TestHappyUCGoVersionModuleTest(HappyUCGoVersionModuleTest):
    pass


class TestHappyUCGoNetModuleTest(HappyUCGoNetModuleTest):
    pass


class TestHappyUCGoPersonalModuleTest(HappyUCGoPersonalModuleTest):
    pass
