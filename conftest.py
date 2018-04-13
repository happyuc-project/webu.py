import pytest
import time

from webu.providers.eth_tester import (
    EthereumTesterProvider,
)
from webu.utils.threads import (
    Timeout,
)
from webu.main import Webu


class PollDelayCounter:
    def __init__(self, initial_delay=0, max_delay=1, initial_step=0.01):
        self.initial_delay = initial_delay
        self.initial_step = initial_step
        self.max_delay = max_delay
        self.current_delay = initial_delay

    def __call__(self):
        delay = self.current_delay

        if self.current_delay == 0:
            self.current_delay += self.initial_step
        else:
            self.current_delay *= 2
            self.current_delay = min(self.current_delay, self.max_delay)

        return delay

    def reset(self):
        self.current_delay = self.initial_delay


@pytest.fixture()
def sleep_interval():
    return PollDelayCounter()


def is_all_testrpc_providers(providers):
    return all(
        isinstance(provider, EthereumTesterProvider)
        for provider
        in providers
    )


@pytest.fixture()
def skip_if_testrpc():

    def _skip_if_testrpc(webu):
        if is_all_testrpc_providers(webu.providers):
            pytest.skip()
    return _skip_if_testrpc


@pytest.fixture()
def wait_for_miner_start():
    def _wait_for_miner_start(webu, timeout=60):
        poll_delay_counter = PollDelayCounter()
        with Timeout(timeout) as timeout:
            while not webu.eth.mining or not webu.eth.hashrate:
                time.sleep(poll_delay_counter())
                timeout.check()
    return _wait_for_miner_start


@pytest.fixture()
def wait_for_block():
    def _wait_for_block(webu, block_number=1, timeout=None):
        if not timeout:
            timeout = (block_number - webu.eth.blockNumber) * 3
        poll_delay_counter = PollDelayCounter()
        with Timeout(timeout) as timeout:
            while True:
                if webu.eth.blockNumber >= block_number:
                    break
                webu.manager.request_blocking("evm_mine", [])
                timeout.sleep(poll_delay_counter())
    return _wait_for_block


@pytest.fixture()
def wait_for_transaction():
    def _wait_for_transaction(webu, txn_hash, timeout=120):
        poll_delay_counter = PollDelayCounter()
        with Timeout(timeout) as timeout:
            while True:
                txn_receipt = webu.eth.getTransactionReceipt(txn_hash)
                if txn_receipt is not None:
                    break
                time.sleep(poll_delay_counter())
                timeout.check()

        return txn_receipt
    return _wait_for_transaction


@pytest.fixture()
def webu():
    provider = EthereumTesterProvider()
    w3 = Webu(provider)

    # Delete this whole block after eth-account has passed security audit
    try:
        w3.eth.account
    except AttributeError:
        pass
    else:
        raise AssertionError("Unaudited features must be disabled by default")
    w3.eth.enable_unaudited_features()

    return w3
