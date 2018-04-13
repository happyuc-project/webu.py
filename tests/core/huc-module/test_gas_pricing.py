from unittest.mock import (
    Mock,
)


def test_no_gas_price_strategy_returns_none(webu):
    assert webu.eth.generateGasPrice() is None


def test_set_gas_price_strategy(webu):
    def my_gas_price_strategy(webu, transaction_params):
        return 5
    webu.eth.setGasPriceStrategy(my_gas_price_strategy)
    assert webu.eth.generateGasPrice() == 5


def test_gas_price_strategy_calls(webu):
    transaction = {
        'to': '0x0',
        'value': 1000000000
    }
    my_gas_price_strategy = Mock(return_value=5)
    webu.eth.setGasPriceStrategy(my_gas_price_strategy)
    assert webu.eth.generateGasPrice(transaction) == 5
    my_gas_price_strategy.assert_called_once_with(webu, transaction)
