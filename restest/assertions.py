import json

def http_status_code(response, code):
    assert response.status_code == code, \
        f"Expecting status code {code} == {response.status_code}"

def contains_text(response, text):
    assert text in response.text, \
        f"Expecting {text} in {response.text}"

def valid_json(response):
    json.loads(response.text), \
        f"Expecting {response.json()} is a JSON"

def contains_field(response):
    pass

def contains_dict(response):
    pass

def matches(response):
    pass
