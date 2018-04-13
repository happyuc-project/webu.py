from webu import Webu
from webu.providers import (
    AutoProvider,
    BaseProvider,
)


class ConnectedProvider(BaseProvider):
    def isConnected(self):
        return True


class DisconnectedProvider(BaseProvider):
    def isConnected(self):
        return False


def test_isConnected_connected():
    """
    Webu.isConnected() returns True when connected to a node.
    """
    webu = Webu(ConnectedProvider())
    assert webu.isConnected() is True


def test_isConnected_disconnected():
    """
    Webu.isConnected() returns False when configured with a provider
    that's not connected to a node.
    """
    webu = Webu(DisconnectedProvider())
    assert webu.isConnected() is False


def test_autoprovider_detection():
    def no_provider():
        return None

    def must_not_call():
        assert False

    auto = AutoProvider([
        no_provider,
        DisconnectedProvider,
        ConnectedProvider,
        must_not_call,
    ])

    w3 = Webu(auto)

    assert w3.isConnected()

    assert isinstance(auto._active_provider, ConnectedProvider)
