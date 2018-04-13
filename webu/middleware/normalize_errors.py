from cytoolz import (
    assoc,
    dissoc,
)


def normalize_errors_middleware(make_request, webu):
    def middleware(method, params):
        result = make_request(method, params)

        # As of v1.8, Ghuc returns errors when you request a
        # receipt for a transaction that is not in the chain.
        # It used to return a result of None, so we simulate the old behavior.

        if method == 'eth_getTransactionReceipt' and 'error' in result:
            is_ghuc = webu.version.node.startswith('Ghuc')
            if is_ghuc and result['error']['code'] == -32000:
                return assoc(
                    dissoc(result, 'error'),
                    'result',
                    None,
                )
            else:
                return result
        else:
            return result
    return middleware
