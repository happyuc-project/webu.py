from eth_utils import (
    apply_to_return_value,
    add_0x_prefix,
    from_wei,
    is_address,
    is_checksum_address,
    keccak,
    remove_0x_prefix,
    to_checksum_address,
    to_wei,
)

from ens import ENS

from webu.admin import Admin
from webu.eth import Eth
from webu.iban import Iban
from webu.miner import Miner
from webu.net import Net
from webu.parity import Parity
from webu.personal import Personal
from webu.testing import Testing
from webu.txpool import TxPool
from webu.version import Version

from webu.providers.ipc import (
    IPCProvider,
)
from webu.providers.rpc import (
    HTTPProvider,
)
from webu.providers.tester import (
    TestRPCProvider,
    HappyUCTesterProvider,
)
from webu.providers.websocket import (
    WebsocketProvider
)

from webu.manager import (
    RequestManager,
)

from webu.utils.abi import (
    map_abi_data,
)
from hexbytes import (
    HexBytes,
)
from webu.utils.decorators import (
    combomethod,
)
from webu.utils.empty import empty
from webu.utils.encoding import (
    hex_encode_abi_type,
    to_bytes,
    to_int,
    to_hex,
    to_text,
)
from webu.utils.normalizers import (
    abi_ens_resolver,
)


def get_default_modules():
    return {
        "eth": Eth,
        "net": Net,
        "personal": Personal,
        "version": Version,
        "txpool": TxPool,
        "miner": Miner,
        "admin": Admin,
        "parity": Parity,
        "testing": Testing,
    }


class Webu:
    # Providers
    HTTPProvider = HTTPProvider
    IPCProvider = IPCProvider
    TestRPCProvider = TestRPCProvider
    HappyUCTesterProvider = HappyUCTesterProvider
    WebsocketProvider = WebsocketProvider

    # Managers
    RequestManager = RequestManager

    # Iban
    Iban = Iban

    # Encoding and Decoding
    toBytes = staticmethod(to_bytes)
    toInt = staticmethod(to_int)
    toHex = staticmethod(to_hex)
    toText = staticmethod(to_text)

    # Currency Utility
    toWei = staticmethod(to_wei)
    fromWei = staticmethod(from_wei)

    # Address Utility
    isAddress = staticmethod(is_address)
    isChecksumAddress = staticmethod(is_checksum_address)
    toChecksumAddress = staticmethod(to_checksum_address)

    def __init__(self, providers=empty, middlewares=None, modules=None, ens=empty):
        self.manager = RequestManager(self, providers, middlewares)

        if modules is None:
            modules = get_default_modules()

        for module_name, module_class in modules.items():
            module_class.attach(self, module_name)

        self.ens = ens

    @property
    def middleware_stack(self):
        return self.manager.middleware_stack

    @property
    def providers(self):
        return self.manager.providers

    @providers.setter
    def providers(self, providers):
        self.manager.providers = providers

    @staticmethod
    @apply_to_return_value(HexBytes)
    def sha3(primitive=None, text=None, hexstr=None):
        if isinstance(primitive, (bytes, int, type(None))):
            input_bytes = to_bytes(primitive, hexstr=hexstr, text=text)
            return keccak(input_bytes)

        raise TypeError(
            "You called sha3 with first arg %r and keywords %r. You must call it with one of "
            "these approaches: sha3(text='txt'), sha3(hexstr='0x747874'), "
            "sha3(b'\\x74\\x78\\x74'), or sha3(0x747874)." % (
                primitive,
                {'text': text, 'hexstr': hexstr}
            )
        )

    @combomethod
    def soliditySha3(cls, abi_types, values):
        """
        Executes sha3 (keccak256) exactly as Solidity does.
        Takes list of abi_types as inputs -- `[uint24, int8[], bool]`
        and list of corresponding values  -- `[20, [-1, 5, 0], True]`
        """
        if len(abi_types) != len(values):
            raise ValueError(
                "Length mismatch between provided abi types and values.  Got "
                "{0} types and {1} values.".format(len(abi_types), len(values))
            )

        if isinstance(cls, type):
            w3 = None
        else:
            w3 = cls
        normalized_values = map_abi_data([abi_ens_resolver(w3)], abi_types, values)

        hex_string = add_0x_prefix(''.join(
            remove_0x_prefix(hex_encode_abi_type(abi_type, value))
            for abi_type, value
            in zip(abi_types, normalized_values)
        ))
        return cls.sha3(hexstr=hex_string)

    def isConnected(self):
        for provider in self.providers:
            if provider.isConnected():
                return True
        else:
            return False

    @property
    def ens(self):
        if self._ens is empty:
            return ENS.fromWebu(self)
        else:
            return self._ens

    @ens.setter
    def ens(self, new_ens):
        self._ens = new_ens
