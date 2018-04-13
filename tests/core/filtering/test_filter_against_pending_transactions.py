import pytest
import random

from flaky import (
    flaky,
)

from webu.utils.threads import (
    Timeout,
)


@pytest.mark.skip(reason="fixture 'webu_empty' not found")
@flaky(max_runs=3)
def test_sync_filter_against_pending_transactions(webu_empty,
                                                  wait_for_transaction,
                                                  skip_if_testrpc
                                                  ):
    webu = webu_empty
    skip_if_testrpc(webu)

    txn_filter = webu.eth.filter("pending")

    txn_1_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 12345,
    })
    txn_2_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 54321,
    })

    wait_for_transaction(webu, txn_1_hash)
    wait_for_transaction(webu, txn_2_hash)

    with Timeout(5) as timeout:
        while not txn_filter.get_new_entries():
            timeout.sleep(random.random())

    seen_txns = txn_filter.get_new_entries()

    assert txn_1_hash in seen_txns
    assert txn_2_hash in seen_txns


@pytest.mark.skip(reason="fixture 'webu_empty' not found")
@flaky(max_runs=3)
def test_async_filter_against_pending_transactions(webu_empty,
                                                   wait_for_transaction,
                                                   skip_if_testrpc
                                                   ):
    webu = webu_empty
    skip_if_testrpc(webu)

    seen_txns = []
    txn_filter = webu.eth.filter("pending")
    txn_filter.watch(seen_txns.append)

    txn_1_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 12345,
    })
    txn_2_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 54321,
    })

    wait_for_transaction(webu, txn_1_hash)
    wait_for_transaction(webu, txn_2_hash)

    with Timeout(5) as timeout:
        while not seen_txns:
            timeout.sleep(random.random())

    txn_filter.stop_watching(30)

    assert txn_1_hash in seen_txns
    assert txn_2_hash in seen_txns
