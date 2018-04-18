
import pytest

from eth_utils import (
    decode_hex,
)

# Ignore warning in pyhappyuc 1.6 - will go away with the upgrade
pytestmark = pytest.mark.filterwarnings("ignore:implicit cast from 'char *'")


def test_contract_deployment_no_constructor(webu, MathContract,
                                            MATH_RUNTIME):
    deploy_txn = MathContract.deploy()

    txn_receipt = webu.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = webu.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(MATH_RUNTIME)


def test_contract_deployment_with_constructor_without_args(webu,
                                                           SimpleConstructorContract,
                                                           SIMPLE_CONSTRUCTOR_RUNTIME):
    deploy_txn = SimpleConstructorContract.deploy()

    txn_receipt = webu.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = webu.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(SIMPLE_CONSTRUCTOR_RUNTIME)


def test_contract_deployment_with_constructor_with_arguments(webu,
                                                             WithConstructorArgumentsContract,
                                                             WITH_CONSTRUCTOR_ARGUMENTS_RUNTIME):
    deploy_txn = WithConstructorArgumentsContract.deploy(args=[1234, 'abcd'])

    txn_receipt = webu.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = webu.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(WITH_CONSTRUCTOR_ARGUMENTS_RUNTIME)


def test_contract_deployment_with_constructor_with_address_argument(webu,
                                                                    WithConstructorAddressArgumentsContract,  # noqa: E501
                                                                    WITH_CONSTRUCTOR_ADDRESS_RUNTIME):  # noqa: E501
    deploy_txn = WithConstructorAddressArgumentsContract.deploy(
        args=["0x16D9983245De15E7A9A73bC586E01FF6E08dE737"],
    )

    txn_receipt = webu.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = webu.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(WITH_CONSTRUCTOR_ADDRESS_RUNTIME)
