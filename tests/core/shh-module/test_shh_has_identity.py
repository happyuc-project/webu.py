def test_shh_has_identity(webu, skip_if_testrpc):
    skip_if_testrpc(webu)
    new_identity = webu.shh.newIdentity()
    assert isinstance(new_identity, bytes)
    assert len(new_identity) == 60
    assert webu.shh.hasIdentity(new_identity)
