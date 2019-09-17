
from assertion import http_status_code, contains_text, valid_json
from actions import do_send

def test_create_post_success_http_201():
    data = ''
    for response in do_send('post', "https://jsonplaceholder.typicode.com", data):
        http_status_code(response, '200')
        contains_text(response, 'text')
        valid_json(response)
