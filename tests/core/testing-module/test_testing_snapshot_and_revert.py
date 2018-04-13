def test_snapshot_revert_to_latest_snapshot(webu):
    webu.testing.mine(5)

    block_before_snapshot = webu.eth.getBlock("latest")

    webu.testing.snapshot()

    block_after_snapshot = webu.eth.getBlock("latest")

    webu.testing.mine(3)

    block_after_mining = webu.eth.getBlock("latest")

    webu.testing.revert()

    block_after_revert = webu.eth.getBlock("latest")

    assert block_after_mining['number'] > block_before_snapshot['number']
    assert block_before_snapshot['hash'] == block_after_snapshot['hash']
    assert block_after_snapshot['hash'] == block_after_revert['hash']


def test_snapshot_revert_to_specific(webu):
    webu.testing.mine(5)

    block_before_snapshot = webu.eth.getBlock("latest")

    snapshot_idx = webu.testing.snapshot()

    block_after_snapshot = webu.eth.getBlock("latest")

    webu.testing.mine()
    webu.testing.snapshot()
    webu.testing.mine()
    webu.testing.snapshot()
    webu.testing.mine()
    webu.testing.snapshot()

    block_after_mining = webu.eth.getBlock("latest")

    webu.testing.revert(snapshot_idx)

    block_after_revert = webu.eth.getBlock("latest")

    assert block_after_mining['number'] > block_before_snapshot['number']
    assert block_before_snapshot['hash'] == block_after_snapshot['hash']
    assert block_after_snapshot['hash'] == block_after_revert['hash']
