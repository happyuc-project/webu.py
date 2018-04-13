import random

from webu.utils.threads import (
    Timeout,
)


def test_txpool_content(webu_empty):
    webu = webu_empty

    webu.miner.stop()

    with Timeout(60) as timeout:
        while webu.miner.hashrate or webu.eth.mining:
            timeout.sleep(random.random())

    txn_1_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 12345,
    })
    txn_1 = webu.eth.getTransaction(txn_1_hash)
    txn_2_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601',
        'value': 54321,
    })
    txn_2 = webu.eth.getTransaction(txn_2_hash)

    content = webu.txpool.content

    assert webu.eth.coinbase in content['pending']

    pending_txns = content['pending'][webu.eth.coinbase]

    assert txn_1['nonce'] in pending_txns
    assert txn_2['nonce'] in pending_txns

    assert pending_txns[txn_1['nonce']][0]['hash'] == txn_1_hash
    assert pending_txns[txn_1['nonce']][0]['value'] == 12345
    assert pending_txns[txn_2['nonce']][0]['hash'] == txn_2_hash
    assert pending_txns[txn_2['nonce']][0]['value'] == 54321
