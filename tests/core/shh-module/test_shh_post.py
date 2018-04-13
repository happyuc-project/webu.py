def test_shh_post(webu, skip_if_testrpc):
    skip_if_testrpc(webu)
    random_topic = "testing"
    assert webu.shh.post({
        "topics": [webu.toHex(text=random_topic)],
        "payload": webu.toHex(text="testing shh on webu.py"),
    })
