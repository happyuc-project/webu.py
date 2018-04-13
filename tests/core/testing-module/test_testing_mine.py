def test_testing_mine_single_block(webu):
    webu.testing.mine()

    before_mining_block = webu.eth.getBlock("latest")

    webu.testing.mine()

    after_mining_block = webu.eth.getBlock("latest")

    assert after_mining_block['number'] - before_mining_block['number'] == 1


def test_testing_mine_multiple_blocks(webu):
    webu.testing.mine()

    before_mining_block = webu.eth.getBlock("latest")

    webu.testing.mine(5)

    after_mining_block = webu.eth.getBlock("latest")

    assert after_mining_block['number'] - before_mining_block['number'] == 5
