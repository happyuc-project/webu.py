import pytest


@pytest.fixture(autouse=True)
def wait_for_first_block(webu, wait_for_block):
    wait_for_block(webu)


@pytest.fixture()
def math_contract(webu,
                  MATH_ABI,
                  MATH_CODE,
                  MATH_RUNTIME,
                  wait_for_transaction):
    MathContract = webu.eth.contract(
        abi=MATH_ABI,
        bytecode=MATH_CODE,
        bytecode_runtime=MATH_RUNTIME,
    )
    deploy_txn = MathContract.deploy({'from': webu.eth.coinbase})
    deploy_receipt = wait_for_transaction(webu, deploy_txn)

    assert deploy_receipt is not None
    contract_address = deploy_receipt['contractAddress']
    webu.isAddress(contract_address)

    _math_contract = MathContract(address=contract_address)
    return _math_contract


@pytest.fixture()
def fallback_function_contract(webu,
                               FALLBACK_FUNCTION_ABI,
                               FALLBACK_FUNCTION_CODE,
                               FALLBACK_FUNCTION_RUNTIME,
                               wait_for_transaction):
    fallback_contract = webu.eth.contract(
        abi=FALLBACK_FUNCTION_ABI,
        bytecode=FALLBACK_FUNCTION_CODE,
        bytecode_runtime=FALLBACK_FUNCTION_RUNTIME
    )
    deploy_txn = fallback_contract.deploy({'from': webu.eth.coinbase})
    deploy_receipt = wait_for_transaction(webu, deploy_txn)

    assert deploy_receipt is not None
    contract_address = deploy_receipt['contractAddress']
    webu.isAddress(contract_address)

    _fallback_function_contract = fallback_contract(address=contract_address)
    return _fallback_function_contract


def test_contract_estimateGas(math_contract, estimateGas):
    gas_estimate = estimateGas(contract=math_contract,
                               contract_function='increment')
    try:
        assert abs(gas_estimate - 21472) < 200  # Ghuc
    except AssertionError:
        assert abs(gas_estimate - 32772) < 200  # eth-tester with py-evm


def test_contract_fallback_estimateGas(fallback_function_contract):
    gas_estimate = fallback_function_contract.fallback.estimateGas()
    try:
        assert abs(gas_estimate - 21472) < 200  # Ghuc
    except AssertionError:
        assert abs(gas_estimate - 29910) < 200  # eth-tester with py-evm


def test_contract_estimateGas_with_arguments(webu, math_contract, estimateGas):
    gas_estimate = estimateGas(contract=math_contract,
                               contract_function='add',
                               func_args=[5, 6])
    try:
        assert abs(gas_estimate - 21984) < 200  # Ghuc
    except AssertionError:
        assert abs(gas_estimate - 30000) < 200  # eth-tester with py-evm
        pass
