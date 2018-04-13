import os
import pytest
import tempfile

from tests.integration.parity.utils import (
    wait_for_socket,
)
from webu import Webu
from webu.utils.module_testing import (
    NetModuleTest,
    VersionModuleTest,
)

from .common import (
    ParityEthModuleTest,
    ParityPersonalModuleTest,
    ParityWebuModuleTest,
)


@pytest.fixture(scope='module')
def ipc_path(datadir):
    ipc_dir_path = tempfile.mkdtemp()
    _ipc_path = os.path.join(ipc_dir_path, 'jsonrpc.ipc')
    yield _ipc_path

    if os.path.exists(_ipc_path):
        os.remove(_ipc_path)


@pytest.fixture(scope="module")
def parity_command_arguments(
    parity_import_blocks_process,
    parity_binary,
    ipc_path,
    datadir,
    passwordfile,
    author
):
    return (
        parity_binary,
        '--chain', os.path.join(datadir, 'chain_config.json'),
        '--ipc-path', ipc_path,
        '--base-path', datadir,
        '--unlock', author,
        '--password', passwordfile,
        '--no-jsonrpc',
        '--no-ws',
    )


@pytest.fixture(scope="module")
def parity_import_blocks_command(parity_binary, ipc_path, datadir, passwordfile):
    return (
        parity_binary,
        'import', os.path.join(datadir, 'blocks_export.rlp'),
        '--chain', os.path.join(datadir, 'chain_config.json'),
        '--ipc-path', ipc_path,
        '--base-path', datadir,
        '--password', passwordfile,
        '--no-jsonrpc',
        '--no-ws',
    )


@pytest.fixture(scope="module")  # noqa: F811
def webu(parity_process, ipc_path):
    wait_for_socket(ipc_path)
    _webu = Webu(Webu.IPCProvider(ipc_path))
    return _webu


class TestParityWebuModuleTest(ParityWebuModuleTest):
    pass


class TestParityEthModuleTest(ParityEthModuleTest):
    pass


class TestParityVersionModule(VersionModuleTest):
    pass


class TestParityNetModule(NetModuleTest):
    pass


class TestParityPersonalModuleTest(ParityPersonalModuleTest):
    pass
