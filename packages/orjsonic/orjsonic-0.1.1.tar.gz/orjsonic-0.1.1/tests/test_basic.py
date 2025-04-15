import orjsonic


def test_loads():
    data = b'{"a": 1, "b": 2}'
    assert orjsonic.loads(data) == {"a": 1, "b": 2}


def test_dumps():
    data = {"a": 1, "b": 2}
    assert orjsonic.dumps(data) == b'{"a":1,"b":2}'
