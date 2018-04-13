import random

from flaky import (
    flaky,
)

from webu.utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_start(webu_empty, wait_for_miner_start):
    webu = webu_empty

    # sanity
    assert webu.eth.mining
    assert webu.miner.hashrate

    webu.miner.stop()

    with Timeout(60) as timeout:
        while webu.eth.mining or webu.eth.hashrate:
            timeout.sleep(random.random())

    assert not webu.eth.mining
    assert not webu.miner.hashrate

    webu.miner.start(1)

    wait_for_miner_start(webu)

    assert webu.eth.mining
    assert webu.miner.hashrate
