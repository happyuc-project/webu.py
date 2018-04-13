import random

from eth_utils import (
    decode_hex,
)
from flaky import (
    flaky,
)

from webu.utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_setExtra(webu_empty, wait_for_block):
    webu = webu_empty

    initial_extra = decode_hex(webu.eth.getBlock(webu.eth.blockNumber)['extraData'])

    new_extra_data = b'-this-is-32-bytes-of-extra-data-'

    # sanity
    assert initial_extra != new_extra_data

    webu.miner.setExtra(new_extra_data)

    with Timeout(60) as timeout:
        while True:
            extra_data = decode_hex(webu.eth.getBlock(webu.eth.blockNumber)['extraData'])
            if extra_data == new_extra_data:
                break
            timeout.sleep(random.random())

    after_extra = decode_hex(webu.eth.getBlock(webu.eth.blockNumber)['extraData'])

    assert after_extra == new_extra_data
