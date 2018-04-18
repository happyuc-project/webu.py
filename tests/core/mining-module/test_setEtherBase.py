
def test_miner_setcoinbase(webu_empty):
    webu = webu_empty
    assert webu.eth.coinbase == webu.eth.accounts[0]
    new_account = webu.personal.newAccount('this-is-a-password')
    webu.miner.setCoinBase(new_account)
    assert webu.eth.coinbase == new_account
