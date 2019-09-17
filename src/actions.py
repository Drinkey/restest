import requests

def do_send(method, url, test_data):
    resp = list()
    for d in test_data:
        func = getattr(requests, method)
        resp.append(func(url=url, json=d))
    return resp
