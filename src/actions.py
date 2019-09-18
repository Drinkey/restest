import requests

def request(method, url, **kwargs):
    return requests.request(method=method, url=url, **kwargs)

def readfile(path):
    return path

def execute(cmd):
    return cmd