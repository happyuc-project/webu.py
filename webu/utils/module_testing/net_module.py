from eth_utils import (
    is_boolean,
    is_integer,
    is_string,
)


class NetModuleTest:
    def test_net_version(self, webu):
        version = webu.net.version

        assert is_string(version)
        assert version.isdigit()

    def test_net_listening(self, webu):
        listening = webu.net.listening

        assert is_boolean(listening)

    def test_net_peerCount(self, webu):
        peer_count = webu.net.peerCount

        assert is_integer(peer_count)
