def test_admin_nodeInfo(webu, skip_if_testrpc):
    skip_if_testrpc(webu)

    node_info = webu.admin.nodeInfo

    assert 'enode' in node_info
    assert 'id' in node_info
