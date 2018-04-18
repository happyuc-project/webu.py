from webu.module import (
    Module,
)


class Miner(Module):
    @property
    def hashrate(self):
        return self.webu.manager.request_blocking("eth_hashrate", [])

    def makeDAG(self, number):
        return self.webu.manager.request_blocking("miner_makeDag", [number])

    def setExtra(self, extra):
        return self.webu.manager.request_blocking("miner_setExtra", [extra])

    def setCoinBase(self, coinbase):
        return self.webu.manager.request_blocking("miner_setcoinbase", [coinbase])

    def setGasPrice(self, gas_price):
        return self.webu.manager.request_blocking(
            "miner_setGasPrice", [gas_price],
        )

    def start(self, num_threads):
        return self.webu.manager.request_blocking(
            "miner_start", [num_threads],
        )

    def stop(self):
        return self.webu.manager.request_blocking("miner_stop", [])

    def startAutoDAG(self):
        return self.webu.manager.request_blocking("miner_startAutoDag", [])

    def stopAutoDAG(self):
        return self.webu.manager.request_blocking("miner_stopAutoDag", [])
