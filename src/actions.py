import requests

def request(method, url, test_data=None):
    resp = list()
    func = getattr(requests, method)
    if not test_data:
        resp.append(func(url=url))
        return resp

    for d in test_data:
        resp.append(func(url=url, json=d))
    return resp

def readfile(path):
    return path

def execute(cmd):
    return cmd