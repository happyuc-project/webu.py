from webu.module import (
    Module,
)


class Parity(Module):
    """
    https://paritytech.github.io/wiki/JSONRPC-parity-module
    """
    def enode(self):
        return self.webu.manager.request_blocking(
            "parity_enode",
            [],
        )

    def netPeers(self):
        return self.webu.manager.request_blocking(
            "parity_netPeers",
            [],
        )
