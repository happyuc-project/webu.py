from webu.module import (
    Module,
)


class Admin(Module):
    def addPeer(self, node_url):
        return self.webu.manager.request_blocking(
            "admin_addPeer", [node_url],
        )

    @property
    def datadir(self):
        return self.webu.manager.request_blocking("admin_datadir", [])

    @property
    def nodeInfo(self):
        return self.webu.manager.request_blocking("admin_nodeInfo", [])

    @property
    def peers(self):
        return self.webu.manager.request_blocking("admin_peers", [])

    def setSolc(self, solc_path):
        return self.webu.manager.request_blocking(
            "admin_setSolc", [solc_path],
        )

    def startRPC(self, host='localhost', port='8545', cors="", apis="eth,net,webu"):
        return self.webu.manager.request_blocking(
            "admin_startRPC",
            [host, port, cors, apis],
        )

    def startWS(self, host='localhost', port='8546', cors="", apis="eth,net,webu"):
        return self.webu.manager.request_blocking(
            "admin_startWS",
            [host, port, cors, apis],
        )

    def stopRPC(self):
        return self.webu.manager.request_blocking("admin_stopRPC", [])

    def stopWS(self):
        return self.webu.manager.request_blocking("admin_stopWS", [])
