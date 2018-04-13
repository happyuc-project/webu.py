import random

from flaky import (
    flaky,
)

from webu.utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_stop(webu_empty):
    webu = webu_empty

    assert webu.eth.mining
    assert webu.miner.hashrate

    webu.miner.stop()

    with Timeout(60) as timeout:
        while webu.eth.mining or webu.eth.hashrate:
            timeout.sleep(random.random())
            timeout.check()

    assert not webu.eth.mining
    assert not webu.miner.hashrate
