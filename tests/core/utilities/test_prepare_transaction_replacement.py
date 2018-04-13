import pytest

from webu.utils.transactions import (
    prepare_replacement_transaction,
)

SIMPLE_CURRENT_TRANSACTION = {
    'blockHash': None,
    'hash': '0x0',
    'nonce': 2,
    'gasPrice': 10,
}


def test_prepare_transaction_replacement(webu):
    current_transaction = SIMPLE_CURRENT_TRANSACTION
    new_transaction = {
        'value': 1,
        'nonce': 2,
    }
    replacement_transaction = prepare_replacement_transaction(
        webu, current_transaction, new_transaction)

    assert replacement_transaction == {
        'value': 1,
        'nonce': 2,
        'gasPrice': 11,
    }


def test_prepare_transaction_replacement_without_nonce_sets_correct_nonce(webu):
    current_transaction = SIMPLE_CURRENT_TRANSACTION
    new_transaction = {
        'value': 1,
    }
    replacement_transaction = prepare_replacement_transaction(
        webu, current_transaction, new_transaction)
    assert replacement_transaction == {
        'value': 1,
        'nonce': 2,
        'gasPrice': 11,
    }


def test_prepare_transaction_replacement_already_mined_raises(webu):
    with pytest.raises(ValueError):
        prepare_replacement_transaction(
            webu, {'blockHash': '0xa1a1a1', 'hash': '0x0'}, {'value': 2})


def test_prepare_transaction_replacement_nonce_mismatch_raises(webu):
    with pytest.raises(ValueError):
        prepare_replacement_transaction(webu, {
            'blockHash': None,
            'hash': '0x0',
            'nonce': 1,
        }, {
            'nonce': 2,
        })


def test_prepare_transaction_replacement_not_higher_gas_price_raises(webu):
    current_transaction = SIMPLE_CURRENT_TRANSACTION
    new_transaction = {
        'value': 1,
        'gasPrice': 5,
    }
    with pytest.raises(ValueError):
        prepare_replacement_transaction(
            webu, current_transaction, new_transaction)

    # Also raises when equal to the current transaction
    new_transaction['gasPrice'] = 10
    with pytest.raises(ValueError):
        prepare_replacement_transaction(webu, current_transaction, new_transaction)


def test_prepare_transaction_replacement_gas_price_defaulting(webu):
    current_transaction = SIMPLE_CURRENT_TRANSACTION
    new_transaction = {
        'value': 2,
    }
    replacement_transaction = prepare_replacement_transaction(
        webu, current_transaction, new_transaction)

    assert replacement_transaction['gasPrice'] == 11


def test_prepare_transaction_replacement_gas_price_defaulting_when_strategy_higer(webu):

    def higher_gas_price_strategy(webu, txn):
        return 20

    webu.eth.setGasPriceStrategy(higher_gas_price_strategy)

    current_transaction = SIMPLE_CURRENT_TRANSACTION
    new_transaction = {
        'value': 2,
    }

    replacement_transaction = prepare_replacement_transaction(
        webu, current_transaction, new_transaction)

    assert replacement_transaction['gasPrice'] == 20


def test_prepare_transaction_replacement_gas_price_defaulting_when_strategy_lower(webu):

    def lower_gas_price_strategy(webu, txn):
        return 5

    webu.eth.setGasPriceStrategy(lower_gas_price_strategy)

    current_transaction = SIMPLE_CURRENT_TRANSACTION
    new_transaction = {
        'value': 2,
    }

    replacement_transaction = prepare_replacement_transaction(
        webu, current_transaction, new_transaction)

    assert replacement_transaction['gasPrice'] == 11
