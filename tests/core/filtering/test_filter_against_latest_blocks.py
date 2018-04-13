from webu.providers.eth_tester import (
    EthereumTesterProvider,
)
from webu.utils.threads import (
    Timeout,
)


def test_sync_filter_against_latest_blocks(webu, sleep_interval, wait_for_block):
    if EthereumTesterProvider not in map(type, webu.providers):
        webu.providers = EthereumTesterProvider()

    txn_filter = webu.eth.filter("latest")

    current_block = webu.eth.blockNumber

    wait_for_block(webu, current_block + 3)

    found_block_hashes = []
    with Timeout(5) as timeout:
        while len(found_block_hashes) < 3:
            found_block_hashes.extend(txn_filter.get_new_entries())
            timeout.sleep(sleep_interval())

    assert len(found_block_hashes) == 3

    expected_block_hashes = [
        webu.eth.getBlock(n + 1).hash for n in range(current_block, current_block + 3)
    ]
    assert found_block_hashes == expected_block_hashes
