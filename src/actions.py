import requests

def request(method, url, test_data):
    resp = list()
    for d in test_data:
        func = getattr(requests, method)
        resp.append(func(url=url, json=d))
    return resp

def readfile(path):
    return path