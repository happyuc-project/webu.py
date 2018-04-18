from webu import Webu
from webu.providers.auto import (
    AutoProvider,
)
from webu.providers.eth_tester import (
    HappyUCTesterProvider,
)


def test_set_providers(webu):
    providers = [HappyUCTesterProvider()]

    webu.providers = providers

    assert webu.providers == providers


def test_set_providers_single(webu):
    providers = [HappyUCTesterProvider()]

    webu.providers = providers[0]

    assert webu.providers == providers


def test_auto_provider_none():
    # init without provider succeeds, even when no provider available
    w3 = Webu()

    # non-node requests succeed
    w3.toHex(0) == '0x0'

    type(w3.providers[0]) == AutoProvider
