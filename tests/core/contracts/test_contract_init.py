import pytest

from webu.exceptions import (
    BadFunctionCallOutput,
    NameNotFound,
)
from webu.utils.ens import (
    contract_ens_addresses,
    ens_addresses,
)


@pytest.fixture
def math_addr(MathContract):
    webu = MathContract.webu
    deploy_txn = MathContract.deploy({'from': webu.eth.coinbase})
    deploy_receipt = webu.eth.getTransactionReceipt(deploy_txn)
    assert deploy_receipt is not None
    return deploy_receipt['contractAddress']


def test_contract_with_unset_address(MathContract):
    with contract_ens_addresses(MathContract, []):
        with pytest.raises(NameNotFound):
            MathContract(address='unsetname.eth')


def test_contract_with_name_address(MathContract, math_addr):
    with contract_ens_addresses(MathContract, [('thedao.eth', math_addr)]):
        mc = MathContract(address='thedao.eth')
        caller = mc.webu.eth.coinbase
        assert mc.address == 'thedao.eth'
        assert mc.functions.return13().call({'from': caller}) == 13


def test_contract_with_name_address_from_eth_contract(
    webu,
    MATH_ABI,
    MATH_CODE,
    MATH_RUNTIME,
    math_addr,
):
    with ens_addresses(webu, [('thedao.eth', math_addr)]):
        mc = webu.eth.contract(
            address='thedao.eth',
            abi=MATH_ABI,
            bytecode=MATH_CODE,
            bytecode_runtime=MATH_RUNTIME,
        )

        caller = mc.webu.eth.coinbase
        assert mc.address == 'thedao.eth'
        assert mc.functions.return13().call({'from': caller}) == 13


def test_contract_with_name_address_changing(MathContract, math_addr):
    # Contract address is validated once on creation
    with contract_ens_addresses(MathContract, [('thedao.eth', math_addr)]):
        mc = MathContract(address='thedao.eth')

    caller = mc.webu.eth.coinbase
    assert mc.address == 'thedao.eth'

    # what happen when name returns no address at all
    with contract_ens_addresses(mc, []):
        with pytest.raises(NameNotFound):
            mc.functions.return13().call({'from': caller})

    # what happen when name returns address to different contract
    with contract_ens_addresses(mc, [('thedao.eth', '0x' + '11' * 20)]):
        with pytest.raises(BadFunctionCallOutput):
            mc.functions.return13().call({'from': caller})

    # contract works again when name resolves correctly
    with contract_ens_addresses(mc, [('thedao.eth', math_addr)]):
        assert mc.functions.return13().call({'from': caller}) == 13
