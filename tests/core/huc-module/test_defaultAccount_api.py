import pytest


@pytest.fixture(autouse=True)
def wait_for_first_block(webu, wait_for_block):
    wait_for_block(webu)


def test_uses_defaultAccount_when_set(webu, extra_accounts,
                                      wait_for_transaction):
    webu.eth.defaultAccount = extra_accounts[2]

    txn_hash = webu.eth.sendTransaction({
        "to": extra_accounts[1],
        "value": 1234,
    })

    wait_for_transaction(webu, txn_hash)

    txn = webu.eth.getTransaction(txn_hash)
    assert txn['from'] == extra_accounts[2]


def test_uses_given_from_address_when_provided(webu, extra_accounts,
                                               wait_for_transaction):
    webu.eth.defaultAccount = extra_accounts[2]
    txn_hash = webu.eth.sendTransaction({
        "from": extra_accounts[5],
        "to": extra_accounts[1],
        "value": 1234,
    })

    wait_for_transaction(webu, txn_hash)

    txn = webu.eth.getTransaction(txn_hash)
    assert txn['from'] == extra_accounts[5]
