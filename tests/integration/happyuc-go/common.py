import pytest
import socket

from webu.utils.module_testing import (
    EthModuleTest,
    NetModuleTest,
    PersonalModuleTest,
    VersionModuleTest,
    WebuModuleTest,
)


def get_open_port():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    return str(port)


class HappyUCGoTest(WebuModuleTest):
    def _check_webu_clientVersion(self, client_version):
        assert client_version.startswith('Ghuc/')


class HappyUCGoEthModuleTest(EthModuleTest):
    def test_eth_replaceTransaction(self, webu, unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction(webu, unlocked_account)

    def test_eth_replaceTransaction_incorrect_nonce(self, webu, unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction_incorrect_nonce(webu, unlocked_account)

    def test_eth_replaceTransaction_gas_price_too_low(self, webu, unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction_gas_price_too_low(webu, unlocked_account)

    def test_eth_replaceTransaction_gas_price_defaulting_minimum(self, webu, unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction_gas_price_defaulting_minimum(webu, unlocked_account)

    def test_eth_replaceTransaction_gas_price_defaulting_strategy_higher(self,
                                                                         webu,
                                                                         unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction_gas_price_defaulting_strategy_higher(
            webu, unlocked_account
        )

    def test_eth_replaceTransaction_gas_price_defaulting_strategy_lower(self,
                                                                        webu,
                                                                        unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction_gas_price_defaulting_strategy_lower(
            webu, unlocked_account
        )

    def test_eth_modifyTransaction(self, webu, unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_modifyTransaction(webu, unlocked_account)


class HappyUCGoVersionModuleTest(VersionModuleTest):
    pass


class HappyUCGoNetModuleTest(NetModuleTest):
    pass


class HappyUCGoPersonalModuleTest(PersonalModuleTest):
    pass
