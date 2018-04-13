
from ens.utils import (
    init_webu,
)


def test_init_adds_middlewares():
    w3 = init_webu()
    middlewares = map(str, w3.manager.middleware_stack)
    assert 'stalecheck_middleware' in next(middlewares)
