import random

from flaky import (
    flaky,
)

from webu.utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_setGasPrice(webu_empty, wait_for_block):
    webu = webu_empty

    initial_gas_price = webu.eth.gasPrice

    # sanity check
    assert webu.eth.gasPrice > 1000

    webu.miner.setGasPrice(initial_gas_price // 2)

    with Timeout(60) as timeout:
        while webu.eth.gasPrice == initial_gas_price:
            timeout.sleep(random.random())

    after_gas_price = webu.eth.gasPrice
    assert after_gas_price < initial_gas_price
