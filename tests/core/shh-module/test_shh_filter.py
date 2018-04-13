import time


def test_shh_sync_filter(webu, skip_if_testrpc):
    skip_if_testrpc(webu)
    topic = webu.toHex(text="test")
    shh_filter = webu.shh.filter({"topics": [topic]})

    payloads = []
    payloads.append(str.encode("payload1"))
    webu.shh.post({
        "topics": [topic],
        "payload": webu.toHex(text=payloads[-1]),
    })
    time.sleep(1)

    payloads.append(str.encode("payload2"))
    webu.shh.post({
        "topics": [topic],
        "payload": webu.toHex(text=payloads[-1]),
    })
    time.sleep(1)
    received_messages = shh_filter.get_new_entries()
    assert len(received_messages) > 1

    for message in received_messages:
        assert message["payload"] in payloads


def test_shh_async_filter(webu, skip_if_testrpc):
    skip_if_testrpc(webu)
    received_messages = []
    topic = webu.toHex(text="test")
    shh_filter = webu.shh.filter({"topics": [topic]})
    shh_filter.watch(received_messages.append)

    payloads = []
    payloads.append(str.encode("payload1"))
    webu.shh.post({
        "topics": [topic],
        "payload": webu.toHex(text=payloads[-1]),
    })
    time.sleep(1)

    payloads.append(str.encode("payload2"))
    webu.shh.post({
        "topics": [topic],
        "payload": webu.toHex(text=payloads[-1]),
    })
    time.sleep(1)
    assert len(received_messages) > 1

    for message in received_messages:
        assert message["payload"] in payloads
