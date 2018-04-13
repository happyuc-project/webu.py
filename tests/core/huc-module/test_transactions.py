import pytest

from webu.exceptions import (
    ValidationError,
)
from webu.middleware.simulate_unmined_transaction import (
    unmined_receipt_simulator_middleware,
)


@pytest.mark.parametrize(
    'make_chain_id, expect_success',
    (
        (
            lambda webu: webu.version.network,
            True,
        ),
        (
            lambda webu: int(webu.version.network),
            True,
        ),
        (
            lambda webu: int(webu.version.network) + 1,
            False,
        ),
        (
            lambda webu: str(int(webu.version.network) + 1),
            False,
        ),
    ),
)
def test_send_transaction_with_valid_chain_id(webu, make_chain_id, expect_success):
    transaction = {
        'to': webu.eth.accounts[1],
        'chainId': make_chain_id(webu),
    }
    if expect_success:
        # just be happy that we didn't crash
        webu.eth.sendTransaction(transaction)
    else:
        with pytest.raises(ValidationError) as exc_info:
            webu.eth.sendTransaction(transaction)

        assert 'chain ID' in str(exc_info.value)


def test_unmined_transaction_wait_for_receipt(webu, extra_accounts):
    webu.middleware_stack.add(unmined_receipt_simulator_middleware)
    txn_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 123457
    })
    assert webu.eth.getTransactionReceipt(txn_hash) is None

    txn_receipt = webu.eth.waitForTransactionReceipt(txn_hash)
    assert txn_receipt['transactionHash'] == txn_hash
    assert txn_receipt['blockHash'] is not None
