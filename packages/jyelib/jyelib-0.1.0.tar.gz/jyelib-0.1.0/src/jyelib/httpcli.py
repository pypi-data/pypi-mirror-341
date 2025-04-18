import requests

'''
    http get请求
'''
def http_get(url, params=None, headers=None):
    resp = requests.get(url, params=params, headers=headers)
    if not resp.ok:
        return resp.text
    return resp.json()

'''
    http post请求
'''
def http_post(url, data=None, headers=None):
    resp = requests.post(url, data=data, headers=headers)
    if not resp.ok:
        return resp.text
    return resp.json()