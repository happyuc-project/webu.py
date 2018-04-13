import pytest
import socket

from webu.utils.module_testing import (
    EthModuleTest,
    PersonalModuleTest,
    WebuModuleTest,
)


def get_open_port():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    return str(port)


class ParityWebuModuleTest(WebuModuleTest):
    def _check_webu_clientVersion(self, client_version):
        assert client_version.startswith('Parity/')


class ParityEthModuleTest(EthModuleTest):
    def test_eth_uninstallFilter(self, webu):
        pytest.xfail('eth_uninstallFilter calls to parity always return true')
        super().test_eth_uninstallFilter(webu)

    def test_eth_newBlockFilter(self, webu):
        pytest.xfail('Parity returns latest block on first polling for new blocks')
        super().test_eth_newBlockFilter(webu)

    def test_eth_replaceTransaction(self, webu, unlocked_account):
        pytest.xfail('Needs ability to efficiently control mining')
        super().test_eth_replaceTransaction(webu, unlocked_account)

    def test_eth_replaceTransaction_already_mined(self, webu, unlocked_account):
        pytest.xfail('Parity is not setup to auto mine')
        super().test_eth_replaceTransaction_already_mined(webu, unlocked_account)

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


class ParityPersonalModuleTest(PersonalModuleTest):
    def test_personal_importRawKey(self, webu):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_importRawKey(webu)

    def test_personal_listAccounts(self, webu):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_listAccounts(webu)

    def test_personal_lockAccount(self, webu, unlocked_account):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_lockAccount(webu, unlocked_account)

    def test_personal_unlockAccount_success(self, webu):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_unlockAccount_success(webu)

    def test_personal_unlockAccount_failure(self, webu, unlockable_account):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_unlockAccount_failure(webu, unlockable_account)

    def test_personal_newAccount(self, webu):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_newAccount(webu)

    def test_personal_sendTransaction(
            self,
            webu,
            unlockable_account,
            unlockable_account_pw):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_sendTransaction(
            webu,
            unlockable_account,
            unlockable_account_pw)

    def test_personal_sign_and_ecrecover(
            self,
            webu,
            unlockable_account,
            unlockable_account_pw):
        pytest.xfail('this non-standard json-rpc method is not implemented on parity')
        super().test_personal_sign_and_ecrecover(
            webu,
            unlockable_account,
            unlockable_account_pw)
