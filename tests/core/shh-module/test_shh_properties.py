def test_shh_version(webu, skip_if_testrpc):
    skip_if_testrpc(webu)
    assert webu.shh.version == 2
