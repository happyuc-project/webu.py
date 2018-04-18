import functools
import pytest

from eth_tester import (
    HappyUCTester,
)
from eth_utils import (
    is_checksum_address,
    is_dict,
)

from webu import Webu
from webu.providers.eth_tester import (
    HappyUCTesterProvider,
)
from webu.utils.module_testing import (
    EthModuleTest,
    NetModuleTest,
    PersonalModuleTest,
    VersionModuleTest,
    WebuModuleTest,
)
from webu.utils.module_testing.emitter_contract import (
    EMITTER_ENUM,
)

pytestmark = pytest.mark.filterwarnings("ignore:implicit cast from 'char *'")


@pytest.fixture(scope="module")
def eth_tester():
    _eth_tester = HappyUCTester()
    return _eth_tester


@pytest.fixture(scope="module")
def eth_tester_provider(eth_tester):
    provider = HappyUCTesterProvider(eth_tester)
    return provider


@pytest.fixture(scope="module")
def webu(eth_tester_provider):
    _webu = Webu(eth_tester_provider)
    return _webu


#
# Math Contract Setup
#
@pytest.fixture(scope="module")
def math_contract_deploy_txn_hash(webu, math_contract_factory):
    deploy_txn_hash = math_contract_factory.deploy({'from': webu.eth.coinbase})
    return deploy_txn_hash


@pytest.fixture(scope="module")
def math_contract(webu, math_contract_factory, math_contract_deploy_txn_hash):
    deploy_receipt = webu.eth.getTransactionReceipt(math_contract_deploy_txn_hash)
    assert is_dict(deploy_receipt)
    contract_address = deploy_receipt['contractAddress']
    assert is_checksum_address(contract_address)
    return math_contract_factory(contract_address)


#
# Emitter Contract Setup
#
@pytest.fixture(scope="module")
def emitter_contract_deploy_txn_hash(webu, emitter_contract_factory):
    deploy_txn_hash = emitter_contract_factory.deploy({'from': webu.eth.coinbase})
    return deploy_txn_hash


@pytest.fixture(scope="module")
def emitter_contract(webu, emitter_contract_factory, emitter_contract_deploy_txn_hash):
    deploy_receipt = webu.eth.getTransactionReceipt(emitter_contract_deploy_txn_hash)
    assert is_dict(deploy_receipt)
    contract_address = deploy_receipt['contractAddress']
    assert is_checksum_address(contract_address)
    return emitter_contract_factory(contract_address)


@pytest.fixture(scope="module")
def empty_block(webu):
    webu.testing.mine()
    block = webu.eth.getBlock("latest")
    assert not block['transactions']
    return block


@pytest.fixture(scope="module")
def block_with_txn(webu):
    txn_hash = webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': webu.eth.coinbase,
        'value': 1,
        'gas': 21000,
        'gas_price': 1,
    })
    txn = webu.eth.getTransaction(txn_hash)
    block = webu.eth.getBlock(txn['blockNumber'])
    return block


@pytest.fixture(scope="module")
def mined_txn_hash(block_with_txn):
    return block_with_txn['transactions'][0]


@pytest.fixture(scope="module")
def block_with_txn_with_log(webu, emitter_contract):
    txn_hash = emitter_contract.transact({
        'from': webu.eth.coinbase,
    }).logDouble(which=EMITTER_ENUM['LogDoubleWithIndex'], arg0=12345, arg1=54321)
    txn = webu.eth.getTransaction(txn_hash)
    block = webu.eth.getBlock(txn['blockNumber'])
    return block


@pytest.fixture(scope="module")
def txn_hash_with_log(block_with_txn_with_log):
    return block_with_txn_with_log['transactions'][0]


UNLOCKABLE_PRIVATE_KEY = '0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01'


@pytest.fixture(scope='module')
def unlockable_account_pw(webu):
    return 'webu-testing'


@pytest.fixture(scope='module')
def unlockable_account(webu, unlockable_account_pw):
    account = webu.personal.importRawKey(UNLOCKABLE_PRIVATE_KEY, unlockable_account_pw)
    webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': account,
        'value': webu.toWei(10, 'huc'),
    })
    yield account


@pytest.fixture
def unlocked_account(webu, unlockable_account, unlockable_account_pw):
    webu.personal.unlockAccount(unlockable_account, unlockable_account_pw)
    yield unlockable_account
    webu.personal.lockAccount(unlockable_account)


@pytest.fixture(scope="module")
def funded_account_for_raw_txn(webu):
    account = '0x39EEed73fb1D3855E90Cbd42f348b3D7b340aAA6'
    webu.eth.sendTransaction({
        'from': webu.eth.coinbase,
        'to': account,
        'value': webu.toWei(10, 'huc'),
        'gas': 21000,
        'gas_price': 1,
    })
    return account


class TestHappyUCTesterWebuModule(WebuModuleTest):
    def _check_webu_clientVersion(self, client_version):
        assert client_version.startswith('HappyUCTester/')


def not_implemented(method, exc_type=NotImplementedError):
    @functools.wraps(method)
    def inner(*args, **kwargs):
        with pytest.raises(exc_type):
            method(*args, **kwargs)
    return inner


def disable_auto_mine(func):
    @functools.wraps(func)
    def func_wrapper(self, eth_tester, *args, **kwargs):
        snapshot = eth_tester.take_snapshot()
        eth_tester.disable_auto_mine_transactions()
        try:
            func(self, eth_tester, *args, **kwargs)
        finally:
            eth_tester.enable_auto_mine_transactions()
            eth_tester.mine_block()
            eth_tester.revert_to_snapshot(snapshot)
    return func_wrapper


class TestHappyUCTesterEthModule(EthModuleTest):
    test_eth_sign = not_implemented(EthModuleTest.test_eth_sign, ValueError)

    @disable_auto_mine
    def test_eth_getTransactionReceipt_unmined(self, eth_tester, webu, unlocked_account):
        super().test_eth_getTransactionReceipt_unmined(webu, unlocked_account)

    @disable_auto_mine
    def test_eth_replaceTransaction(self, eth_tester, webu, unlocked_account):
        super().test_eth_replaceTransaction(webu, unlocked_account)

    @disable_auto_mine
    def test_eth_replaceTransaction_incorrect_nonce(self, eth_tester, webu, unlocked_account):
        super().test_eth_replaceTransaction_incorrect_nonce(webu, unlocked_account)

    @disable_auto_mine
    def test_eth_replaceTransaction_gas_price_too_low(self, eth_tester, webu, unlocked_account):
        super().test_eth_replaceTransaction_gas_price_too_low(webu, unlocked_account)

    @disable_auto_mine
    def test_eth_replaceTransaction_gas_price_defaulting_minimum(self,
                                                                 eth_tester,
                                                                 webu,
                                                                 unlocked_account):
        super().test_eth_replaceTransaction_gas_price_defaulting_minimum(webu, unlocked_account)

    @disable_auto_mine
    def test_eth_replaceTransaction_gas_price_defaulting_strategy_higher(self,
                                                                         eth_tester,
                                                                         webu,
                                                                         unlocked_account):
        super().test_eth_replaceTransaction_gas_price_defaulting_strategy_higher(
            webu, unlocked_account
        )

    @disable_auto_mine
    def test_eth_replaceTransaction_gas_price_defaulting_strategy_lower(self,
                                                                        eth_tester,
                                                                        webu,
                                                                        unlocked_account):
        super().test_eth_replaceTransaction_gas_price_defaulting_strategy_lower(
            webu, unlocked_account
        )

    @disable_auto_mine
    def test_eth_modifyTransaction(self, eth_tester, webu, unlocked_account):
        super().test_eth_modifyTransaction(webu, unlocked_account)

    @disable_auto_mine
    def test_eth_call_old_contract_state(self, eth_tester, webu, math_contract, unlocked_account):
        # For now, happyuc tester cannot give call results in the pending block.
        # Once that feature is added, then delete the except/else blocks.
        try:
            super().test_eth_call_old_contract_state(webu, math_contract, unlocked_account)
        except AssertionError as err:
            if str(err) == "pending call result was 0 instead of 1":
                pass
            else:
                raise err
        else:
            raise AssertionError("eth-tester was unexpectedly able to give the pending call result")


class TestHappyUCTesterVersionModule(VersionModuleTest):
    pass


class TestHappyUCTesterNetModule(NetModuleTest):
    pass


class TestHappyUCTesterPersonalModule(PersonalModuleTest):
    test_personal_sign_and_ecrecover = not_implemented(
        PersonalModuleTest.test_personal_sign_and_ecrecover,
        ValueError,
    )
