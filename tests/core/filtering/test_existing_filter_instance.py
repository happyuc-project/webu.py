import pytest

from webu.providers.eth_tester import (
    HappyUCTesterProvider,
)
from webu.utils.threads import (
    Timeout,
)


@pytest.fixture()
def filter_id(webu):
    if HappyUCTesterProvider not in map(type, webu.providers):
        webu.providers = HappyUCTesterProvider()

    block_filter = webu.eth.filter("latest")
    return block_filter.filter_id


def test_instatiate_existing_filter(webu, sleep_interval, wait_for_block, filter_id):
    with pytest.raises(TypeError):
        webu.eth.filter('latest', filter_id)
    with pytest.raises(TypeError):
        webu.eth.filter('latest', filter_id=filter_id)
    with pytest.raises(TypeError):
        webu.eth.filter(filter_params='latest', filter_id=filter_id)

    block_filter = webu.eth.filter(filter_id=filter_id)

    current_block = webu.eth.blockNumber

    wait_for_block(webu, current_block + 3)

    found_block_hashes = []
    with Timeout(5) as timeout:
        while len(found_block_hashes) < 3:
            found_block_hashes.extend(block_filter.get_new_entries())
            timeout.sleep(sleep_interval())

    assert len(found_block_hashes) == 3

    expected_block_hashes = [
        webu.eth.getBlock(n + 1).hash for n in range(current_block, current_block + 3)
    ]
    assert found_block_hashes == expected_block_hashes
