import math

from cytoolz import (
    assoc,
    curry,
    merge,
)

from webu.utils.threads import (
    Timeout,
)

VALID_TRANSACTION_PARAMS = [
    'from',
    'to',
    'gas',
    'gasPrice',
    'value',
    'data',
    'nonce',
    'chainId',
]

TRANSACTION_DEFAULTS = {
    'value': 0,
    'data': b'',
    'gas': lambda webu, tx: webu.eth.estimateGas(tx),
    'gasPrice': lambda webu, tx: webu.eth.generateGasPrice(tx) or webu.eth.gasPrice,
    'chainId': lambda webu, tx: int(webu.net.version),
}


@curry
def fill_transaction_defaults(webu, transaction):
    '''
    if webu is None, fill as much as possible while offline
    '''
    defaults = {}
    for key, default_getter in TRANSACTION_DEFAULTS.items():
        if key not in transaction:
            if callable(default_getter):
                if webu is not None:
                    default_val = default_getter(webu, transaction)
                else:
                    raise ValueError("You must specify %s in the transaction" % key)
            else:
                default_val = default_getter
            defaults[key] = default_val
    return merge(defaults, transaction)


def wait_for_transaction_receipt(webu, txn_hash, timeout=120, poll_latency=0.1):
    with Timeout(timeout) as _timeout:
        while True:
            txn_receipt = webu.eth.getTransactionReceipt(txn_hash)
            if txn_receipt is not None:
                break
            _timeout.sleep(poll_latency)
    return txn_receipt


def get_block_gas_limit(webu, block_identifier=None):
    if block_identifier is None:
        block_identifier = webu.eth.blockNumber
    block = webu.eth.getBlock(block_identifier)
    return block['gasLimit']


def get_buffered_gas_estimate(webu, transaction, gas_buffer=100000):
    gas_estimate_transaction = dict(**transaction)

    gas_estimate = webu.eth.estimateGas(gas_estimate_transaction)

    gas_limit = get_block_gas_limit(webu)

    if gas_estimate > gas_limit:
        raise ValueError(
            "Contract does not appear to be deployable within the "
            "current network gas limits.  Estimated: {0}. Current gas "
            "limit: {1}".format(gas_estimate, gas_limit)
        )

    return min(gas_limit, gas_estimate + gas_buffer)


def get_required_transaction(webu, transaction_hash):
    current_transaction = webu.eth.getTransaction(transaction_hash)
    if not current_transaction:
        raise ValueError('Supplied transaction with hash {} does not exist'
                         .format(transaction_hash))
    return current_transaction


def extract_valid_transaction_params(transaction_params):
    return {key: transaction_params[key]
            for key in VALID_TRANSACTION_PARAMS if key in transaction_params}


def assert_valid_transaction_params(transaction_params):
    for param in transaction_params:
        if param not in VALID_TRANSACTION_PARAMS:
            raise ValueError('{} is not a valid transaction parameter'.format(param))


def prepare_replacement_transaction(webu, current_transaction, new_transaction):
    if current_transaction['blockHash'] is not None:
        raise ValueError('Supplied transaction with hash {} has already been mined'
                         .format(current_transaction['hash']))
    if 'nonce' in new_transaction and new_transaction['nonce'] != current_transaction['nonce']:
        raise ValueError('Supplied nonce in new_transaction must match the pending transaction')

    if 'nonce' not in new_transaction:
        new_transaction = assoc(new_transaction, 'nonce', current_transaction['nonce'])

    if 'gasPrice' in new_transaction:
        if new_transaction['gasPrice'] <= current_transaction['gasPrice']:
            raise ValueError('Supplied gas price must exceed existing transaction gas price')
    else:
        generated_gas_price = webu.eth.generateGasPrice(new_transaction)
        minimum_gas_price = int(math.ceil(current_transaction['gasPrice'] * 1.1))
        if generated_gas_price and generated_gas_price > minimum_gas_price:
            new_transaction = assoc(new_transaction, 'gasPrice', generated_gas_price)
        else:
            new_transaction = assoc(new_transaction, 'gasPrice', minimum_gas_price)

    return new_transaction


def replace_transaction(webu, current_transaction, new_transaction):
    new_transaction = prepare_replacement_transaction(
        webu, current_transaction, new_transaction
    )
    return webu.eth.sendTransaction(new_transaction)
