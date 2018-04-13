def test_time_traveling(webu):
    current_block_time = webu.eth.getBlock("pending")['timestamp']

    time_travel_to = current_block_time + 12345

    webu.testing.timeTravel(time_travel_to)

    latest_block_time = webu.eth.getBlock("pending")['timestamp']
    assert latest_block_time >= time_travel_to
