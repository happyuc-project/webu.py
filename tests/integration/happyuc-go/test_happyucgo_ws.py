import pytest

from tests.integration.utils import (
    wait_for_ws,
)
from webu import Webu

from .common import (
    HappyUCGoEthModuleTest,
    HappyUCGoNetModuleTest,
    HappyUCGoPersonalModuleTest,
    HappyUCGoTest,
    HappyUCGoVersionModuleTest,
    get_open_port,
)


@pytest.fixture(scope="module")
def ws_port():
    return get_open_port()


@pytest.fixture(scope="module")
def endpoint_uri(ws_port):
    return 'ws://localhost:{0}'.format(ws_port)


@pytest.fixture(scope='module')
def ghuc_command_arguments(ghuc_binary, datadir, ws_port):
    return (
        ghuc_binary,
        '--datadir', str(datadir),
        '--nodiscover',
        '--fakepow',
        '--ws',
        '--wsport', ws_port,
        '--wsapi', 'db,eth,net,webu,personal,webu',
        '--wsorigins', '*',
        '--ipcdisable',
    )


@pytest.fixture(scope="module")
def webu(ghuc_process, endpoint_uri, event_loop):
    event_loop.run_until_complete(wait_for_ws(endpoint_uri, event_loop))
    _webu = Webu(Webu.WebsocketProvider(endpoint_uri))
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
