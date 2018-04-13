import pytest

from webu.middleware import (
    construct_fixture_middleware,
    ghuc_poa_middleware,
)


# In the spec, a block with extra data longer than 32 bytes is invalid
def test_long_extra_data(webu):
    return_block_with_long_extra_data = construct_fixture_middleware({
        'eth_getBlockByNumber': {'extraData': '0x' + 'ff' * 33},
    })
    webu.middleware_stack.inject(return_block_with_long_extra_data, layer=0)
    with pytest.raises(ValueError):
        webu.eth.getBlock('latest')


def test_full_extra_data(webu):
    return_block_with_long_extra_data = construct_fixture_middleware({
        'eth_getBlockByNumber': {'extraData': '0x' + 'ff' * 32},
    })
    webu.middleware_stack.inject(return_block_with_long_extra_data, layer=0)
    block = webu.eth.getBlock('latest')
    assert block.extraData == b'\xff' * 32


def test_ghuc_proof_of_authority(webu):
    return_block_with_long_extra_data = construct_fixture_middleware({
        'eth_getBlockByNumber': {'extraData': '0x' + 'ff' * 33},
    })
    webu.middleware_stack.inject(ghuc_poa_middleware, layer=0)
    webu.middleware_stack.inject(return_block_with_long_extra_data, layer=0)
    block = webu.eth.getBlock('latest')
    assert 'extraData' not in block
    assert block.proofOfAuthorityData == b'\xff' * 33
