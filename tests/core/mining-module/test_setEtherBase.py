
def test_miner_setEtherbase(webu_empty):
    webu = webu_empty
    assert webu.eth.coinbase == webu.eth.accounts[0]
    new_account = webu.personal.newAccount('this-is-a-password')
    webu.miner.setEtherBase(new_account)
    assert webu.eth.coinbase == new_account
