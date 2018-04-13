import pytest
from unittest.mock import (
    Mock,
)

ABI = [{}]
ADDRESS = '0xd3CdA913deB6f67967B99D67aCDFa1712C293601'
NON_CHECKSUM_ADDRESS = '0xd3cda913deb6f67967b99d67acdfa1712c293601'
INVALID_CHECKSUM_ADDRESS = '0xd3CDA913deB6f67967B99D67aCDFa1712C293601'


@pytest.mark.parametrize(
    'args,kwargs,expected',
    (
        ((ADDRESS,), {}, None),
        ((INVALID_CHECKSUM_ADDRESS,), {}, ValueError),
        ((NON_CHECKSUM_ADDRESS,), {}, ValueError),
        ((), {'address': ADDRESS}, None),
        ((), {'address': INVALID_CHECKSUM_ADDRESS}, ValueError),
        ((), {'address': NON_CHECKSUM_ADDRESS}, ValueError),
    )
)
def test_contract_address_validation(webu, args, kwargs, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            webu.eth.contract(*args, **kwargs)
        return

    # run without errors
    webu.eth.contract(*args, **kwargs)


def test_set_contract_factory(webu):
    factoryClass = Mock()
    webu.eth.setContractFactory(factoryClass)
    webu.eth.contract(contract_name='myname')
    factoryClass.factory.assert_called_once_with(webu, contract_name='myname')
