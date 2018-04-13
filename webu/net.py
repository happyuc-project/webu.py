from webu.module import (
    Module,
)


class Net(Module):
    @property
    def listening(self):
        return self.webu.manager.request_blocking("net_listening", [])

    @property
    def peerCount(self):
        return self.webu.manager.request_blocking("net_peerCount", [])

    @property
    def chainId(self):
        return self.version

    @property
    def version(self):
        return self.webu.manager.request_blocking("net_version", [])
