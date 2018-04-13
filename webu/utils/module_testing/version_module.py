from eth_utils import (
    is_string,
)


class VersionModuleTest:
    def test_net_version(self, webu):
        version = webu.version.network

        assert is_string(version)
        assert version.isdigit()

    def test_eth_protocolVersion(self, webu):
        protocol_version = webu.version.ethereum

        assert is_string(protocol_version)
        assert protocol_version.isdigit()
