import contextlib
import os
import shutil
import signal
import socket
import subprocess
import tempfile
import time

from eth_utils import (
    is_checksum_address,
    to_text,
)

COINBASE = '0xdc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd'
COINBASE_PK = '0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d'

KEYFILE_DATA = '{"address":"dc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd","crypto":{"cipher":"aes-128-ctr","ciphertext":"52e06bc9397ea9fa2f0dae8de2b3e8116e92a2ecca9ad5ff0061d1c449704e98","cipherparams":{"iv":"aa5d0a5370ef65395c1a6607af857124"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"9fdf0764eb3645ffc184e166537f6fe70516bf0e34dc7311dea21f100f0c9263"},"mac":"4e0b51f42b865c15c485f4faefdd1f01a38637e5247f8c75ffe6a8c0eba856f6"},"id":"5a6124e0-10f1-4c1c-ae3e-d903eacb740a","version":3}'  # noqa: E501

KEYFILE_PW = 'webupy-test'
KEYFILE_FILENAME = 'UTC--2017-08-24T19-42-47.517572178Z--dc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd'  # noqa: E501

RAW_TXN_ACCOUNT = '0x39EEed73fb1D3855E90Cbd42f348b3D7b340aAA6'

UNLOCKABLE_PRIVATE_KEY = '0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01'
UNLOCKABLE_ACCOUNT = '0x12efdc31b1a8fa1a1e756dfd8a1601055c971e13'
UNLOCKABLE_ACCOUNT_PW = KEYFILE_PW

GENESIS_DATA = {
    "config": {
        "chainId": 1337,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip155Block": 10,
        "eip158Block": 10,
        "eip160Block": 10
    },
    "nonce": "0x0000000000000042",
    "alloc": {
        COINBASE: {
            "balance": "1000000000000000000000000000"
        },
        UNLOCKABLE_ACCOUNT: {
            "balance": "1000000000000000000000000000"
        },
        RAW_TXN_ACCOUNT: {
            "balance": "1000000000000000000000000000"
        }
    },
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "0x3535353535353535353535353535353535353535353535353535353535353535",
    "gasLimit": "0x1000000",
    "difficulty": "0x10000",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": COINBASE
}


def ensure_path_exists(dir_path):
    """
    Make sure that a path exists
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False


@contextlib.contextmanager
def tempdir():
    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)


def get_open_port():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    return str(port)


def get_ghuc_binary():
    from ghuc.install import (
        get_executable_path,
        install_ghuc,
    )

    if 'GETH_BINARY' in os.environ:
        return os.environ['GETH_BINARY']
    elif 'GETH_VERSION' in os.environ:
        ghuc_version = os.environ['GETH_VERSION']
        _ghuc_binary = get_executable_path(ghuc_version)
        if not os.path.exists(_ghuc_binary):
            install_ghuc(ghuc_version)
        assert os.path.exists(_ghuc_binary)
        return _ghuc_binary
    else:
        return 'ghuc'


def wait_for_popen(proc, timeout):
    start = time.time()
    while time.time() < start + timeout:
        if proc.poll() is None:
            time.sleep(0.01)
        else:
            break


def kill_proc_gracefully(proc):
    if proc.poll() is None:
        proc.send_signal(signal.SIGINT)
        wait_for_popen(proc, 13)

    if proc.poll() is None:
        proc.terminate()
        wait_for_popen(proc, 5)

    if proc.poll() is None:
        proc.kill()
        wait_for_popen(proc, 2)


def wait_for_socket(ipc_path, timeout=30):
    start = time.time()
    while time.time() < start + timeout:
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(ipc_path)
            sock.settimeout(timeout)
        except (FileNotFoundError, socket.error):
            time.sleep(0.01)
        else:
            break


@contextlib.contextmanager
def get_ghuc_process(ghuc_binary,
                     datadir,
                     genesis_file_path,
                     ipc_path,
                     port,
                     networkid,
                     skip_init=False):
    if not skip_init:
        init_datadir_command = (
            ghuc_binary,
            '--datadir', datadir,
            'init',
            genesis_file_path,
        )
        print(' '.join(init_datadir_command))
        subprocess.check_output(
            init_datadir_command,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    run_ghuc_command = (
        ghuc_binary,
        '--datadir', datadir,
        '--ipcpath', ipc_path,
        '--nodiscover',
        '--port', port,
        '--networkid', networkid,
        '--coinbase', COINBASE[2:],
    )
    print(' '.join(run_ghuc_command))
    try:
        proc = get_process(run_ghuc_command)
        yield proc
    finally:
        kill_proc_gracefully(proc)
        output, errors = proc.communicate()
        print(
            "Ghuc Process Exited:\n"
            "stdout:{0}\n\n"
            "stderr:{1}\n\n".format(
                to_text(output),
                to_text(errors),
            )
        )


def get_process(run_command):
    proc = subprocess.Popen(
        run_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    return proc


def mine_block(webu):
    origin_block_number = webu.eth.blockNumber

    start_time = time.time()
    webu.miner.start(1)
    while time.time() < start_time + 120:
        block_number = webu.eth.blockNumber
        if block_number > origin_block_number:
            webu.miner.stop()
            return block_number
        else:
            time.sleep(0.1)
    else:
        raise ValueError("No block mined during wait period")


def mine_transaction_hash(webu, txn_hash):
    start_time = time.time()
    webu.miner.start(1)
    while time.time() < start_time + 120:
        receipt = webu.eth.getTransactionReceipt(txn_hash)
        if receipt is not None:
            webu.miner.stop()
            return receipt
        else:
            time.sleep(0.1)
    else:
        raise ValueError("Math contract deploy transaction not mined during wait period")


def deploy_contract(webu, name, factory):
    webu.personal.unlockAccount(webu.eth.coinbase, KEYFILE_PW)
    deploy_txn_hash = factory.deploy({'from': webu.eth.coinbase})
    print('{0}_CONTRACT_DEPLOY_HASH: '.format(name.upper()), deploy_txn_hash)
    deploy_receipt = mine_transaction_hash(webu, deploy_txn_hash)
    print('{0}_CONTRACT_DEPLOY_TRANSACTION_MINED'.format(name.upper()))
    contract_address = deploy_receipt['contractAddress']
    assert is_checksum_address(contract_address)
    print('{0}_CONTRACT_ADDRESS:'.format(name.upper()), contract_address)
    return deploy_receipt
