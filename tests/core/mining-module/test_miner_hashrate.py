from flaky import (
    flaky,
)


@flaky(max_runs=3)
def test_miner_hashrate(webu_empty, wait_for_miner_start):
    webu = webu_empty

    hashrate = webu.miner.hashrate
    assert hashrate > 0
