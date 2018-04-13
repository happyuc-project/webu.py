import pytest


@pytest.fixture(autouse=True)
def always_wait_for_mining_start(webu,
                                 wait_for_miner_start,
                                 skip_if_testrpc):
    skip_if_testrpc(webu)

    wait_for_miner_start(webu)

    assert webu.eth.mining
    assert webu.eth.hashrate
    assert webu.miner.hashrate
