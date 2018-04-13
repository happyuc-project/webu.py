from webu.module import (
    Module,
)


class TxPool(Module):
    @property
    def content(self):
        return self.webu.manager.request_blocking("txpool_content", [])

    @property
    def inspect(self):
        return self.webu.manager.request_blocking("txpool_inspect", [])

    @property
    def status(self):
        return self.webu.manager.request_blocking("txpool_status", [])
