def test_admin_peers(webu, skip_if_testrpc):
    skip_if_testrpc(webu)

    assert webu.admin.peers == []
