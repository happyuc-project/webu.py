def test_mining_property_tester(webu):
    assert webu.eth.mining is False


def test_mining_property_ipc_and_rpc(webu, wait_for_miner_start, skip_if_testrpc):
    skip_if_testrpc(webu)

    wait_for_miner_start(webu)
    assert webu.eth.mining is True
