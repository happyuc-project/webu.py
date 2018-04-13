from cytoolz import (
    compose,
)
from eth_utils.curried import (
    apply_formatters_to_dict,
    apply_key_map,
)
from hexbytes import (
    HexBytes,
)

from webu.middleware.formatting import (
    construct_formatting_middleware,
)

remap_ghuc_poa_fields = apply_key_map({
    'extraData': 'proofOfAuthorityData',
})

pythonic_ghuc_poa = apply_formatters_to_dict({
    'proofOfAuthorityData': HexBytes,
})

ghuc_poa_cleanup = compose(pythonic_ghuc_poa, remap_ghuc_poa_fields)

ghuc_poa_middleware = construct_formatting_middleware(
    result_formatters={
        'eth_getBlockByHash': ghuc_poa_cleanup,
        'eth_getBlockByNumber': ghuc_poa_cleanup,
    },
)
