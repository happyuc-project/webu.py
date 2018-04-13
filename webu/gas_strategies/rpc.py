def rpc_gas_price_strategy(webu, transaction_params=None):
    """
    A simple gas price strategy deriving it's value from the eth_gasPrice JSON-RPC call.
    """
    return webu.manager.request_blocking("eth_gasPrice", [])
