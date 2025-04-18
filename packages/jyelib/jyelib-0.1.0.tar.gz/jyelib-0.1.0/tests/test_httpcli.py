from jyelib.httpcli import http_get, http_post


def test_http_get():
    ret = http_get("http://httpbin.org/get")
    print(ret)
    assert type(ret) == dict


def test_http_post():
    ret = http_post("http://httpbin.org/post")
    print(ret)
    assert type(ret) == dict