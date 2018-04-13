from webu.gas_strategies.rpc import (
    rpc_gas_price_strategy,
)


def test_default_rpc_gas_price_strategy(webu):
    assert rpc_gas_price_strategy(webu, {
        'to': '0x0',
        'value': 1
    }) == 1


def test_default_rpc_gas_price_strategy_callable_without_transaction(webu):
    assert rpc_gas_price_strategy(webu) == 1
