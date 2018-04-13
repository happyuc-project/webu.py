import pytest
import subprocess

from eth_utils import (
    to_text,
)


def test_admin_setSolc(webu, skip_if_testrpc):
    skip_if_testrpc(webu)

    try:
        solc_path = subprocess.check_output(['which', 'solc']).strip()
    except subprocess.CalledProcessError:
        pytest.skip('solc binary not found')
    solc_version = subprocess.check_output(['solc', '--version']).strip()

    actual = webu.admin.setSolc(solc_path)
    assert to_text(solc_version) in actual
    assert to_text(solc_path) in actual
