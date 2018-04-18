from webu.module import (
    Module,
)


class Version(Module):
    @property
    def api(self):
        from webu import __version__
        return __version__

    @property
    def node(self):
        return self.webu.manager.request_blocking("webu_clientVersion", [])

    @property
    def network(self):
        return self.webu.manager.request_blocking("net_version", [])

    @property
    def happyuc(self):
        return self.webu.manager.request_blocking("eth_protocolVersion", [])
