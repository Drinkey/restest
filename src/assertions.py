
def http_status_code(response, code):
    assert response.status_code == code

def contains_text(response, text):
    assert text in response.text

def valid_json(response):
    assert isinstance(response.json, dict)