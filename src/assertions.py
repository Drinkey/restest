import json
def http_status_code(response, code):
    try:
        assert response.status_code == code
    except AssertionError as err:
        raise AssertionError(f"Expecting status code {code} == {response.status_code}")

def contains_text(response, text):
    try:
        assert text in response.text
    except AssertionError as err:
        raise AssertionError(f"Expecting {text} in {response.text}")

def valid_json(response):
    try:
        json.loads(response.text)
    except ValueError as err:
        raise AssertionError(f"Expecting {response.json()} is a JSON")

def contains_field(response):
    pass

def contains_dict(response):
    pass

def matches(response):
    pass
