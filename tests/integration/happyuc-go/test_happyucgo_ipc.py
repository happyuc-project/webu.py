import os
import pytest
import tempfile

from webu import Webu

from .common import (
    GoEthereumEthModuleTest,
    GoEthereumNetModuleTest,
    GoEthereumPersonalModuleTest,
    GoEthereumTest,
    GoEthereumVersionModuleTest,
)
from .utils import (
    get_open_port,
    wait_for_socket,
)


@pytest.fixture(scope='module')
def ghuc_command_arguments(ghuc_binary, datadir, ghuc_ipc_path):
    ghuc_port = get_open_port()
    return (
        ghuc_binary,
        '--datadir', str(datadir),
        '--ipcpath', ghuc_ipc_path,
        '--nodiscover',
        '--fakepow',
        '--port', ghuc_port,
    )


@pytest.fixture(scope='module')
def ghuc_ipc_path(datadir):
    ghuc_ipc_dir_path = tempfile.mkdtemp()
    _ghuc_ipc_path = os.path.join(ghuc_ipc_dir_path, 'ghuc.ipc')
    yield _ghuc_ipc_path

    if os.path.exists(_ghuc_ipc_path):
        os.remove(_ghuc_ipc_path)


@pytest.fixture(scope="module")
def webu(ghuc_process, ghuc_ipc_path):
    wait_for_socket(ghuc_ipc_path)
    _webu = Webu(Webu.IPCProvider(ghuc_ipc_path))
    return _webu


class TestGoEthereumTest(GoEthereumTest):
    pass


class TestGoEthereumEthModuleTest(GoEthereumEthModuleTest):
    pass


class TestGoEthereumVersionModuleTest(GoEthereumVersionModuleTest):
    pass


class TestGoEthereumNetModuleTest(GoEthereumNetModuleTest):
    pass


class TestGoEthereumPersonalModuleTest(GoEthereumPersonalModuleTest):
    pass
