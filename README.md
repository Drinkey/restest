# restest

Simple RESTFul API Test Framework for learning, reinventing wheels (don't do it)

---
Table of Contents
- [restest](#restest)
  - [Environment](#environment)
  - [Install](#install)
  - [Writing a test case](#writing-a-test-case)
    - [Assertions](#assertions)
    - [Actions](#actions)
    - [Variables](#variables)
    - [Test Suite](#test-suite)
  - [Command Line Usage](#command-line-usage)
  - [Development](#development)
## Environment

- Python 3.6.5
- Python 3.7.3

## Install

From source:

```shell
$ git clone git@github.com:Drinkey/restest.git
# or
$ git clone https://github.com/Drinkey/restest.git
$ cd restest
$ python setup.py install
```

Using `pip`

```shell
$ pip install git+https://github.com/Drinkey/restest.git
...
```

## Writing a test case

Here is a simple test suite file to describe a test case

```yaml
assertions:
  - http_status_code
  - valid_json

actions:
  - request

variables:
  base_url: https://jsonplaceholder.typicode.com
  url: "{base_url}/posts"
  get: "get"
  post: "post"

testsuite:
  description: Test jsonplaceholder Comment Resources CRUD

  testcases:
    - name: List all jsonplaceholder posts
      do:
        - method: get
          url: url
          expect:
            - http_status_code: 200
            - valid_json
```

Our program will convert it to a pytest script like following and run it by pytest

```python
"""Test jsonplaceholder Comment Resources CRUD
"""
from assertions import http_status_code, valid_json

from actions import request

base_url = 'https://jsonplaceholder.typicode.com'
url = f'{base_url}/posts'
get = 'get'
post = 'post'

def test_list_all_jsonplaceholder_posts():
    response = request(method=get, url=url)
    http_status_code(response, 200)
    valid_json(response)
```

Let's break it down into pieces

### Assertions

Assertions is a list of functions that you want to include for doing result validation in the current test suite. When validation failed, `AssertionError` will be raised.

Assertion functions can be found in `restest/assertions.py`, and you can also add your own assertion functions by adding functions to this file.

Right now, we only provide 3 assertion functions:
- `http_status_code`
- `contains_text`
- `valid_json`

They all take the `response` as the first parameter, and when calling them in the `expect` section of a test case, the key is defining which assertion to call, and value is what is the second parameter of assertion functions.

For example, we have a assertion function `http_status_code` 
```python
def http_status_code(response, code):
    assert response.status_code == code, \
        f"Expecting status code {code} == {response.status_code}"
```

After we include it in this test suite file, 

```yaml
assertions:
  - http_status_code
  - valid_json
```

we can call it in test case `expect` section

```yaml
    - name: List all jsonplaceholder posts
      do:
        - method: get
          url: url
          expect:
            - http_status_code: 200
            - valid_json
```

The `expect` is specifying a list of validation. Each validation is a `dict` or `str`. When the validation is a dict, the key is validation function to call, and the value is the parameter we want to pass. If the validation is a `str`, it's the validation function we want to call. The parameter `response` will be passed by default no matter the validation is a `dict` or a `str`.

In this case, we have called 2 validation, one is `http_status_code` to check whether response status code is 200. If the validation fails, `AssertionError` will be raised. And another is `valid_json` to validate the response is a valid JSON. If the response is not a valid JSON, `AssertionError` will be raised.

### Actions

Actions is a list of test functions you want to run, for example, send a HTTP request, send out a TCP packet, creating a test file, etc. Actions function can be found in `restest/actions.py`

```yaml
actions:
  - request
```
This means to import `request` (without `s`) to this test suite which will be called in the test cases.

In the test case section, `do` is a list of operations to run a test step and validate result.
```yaml
      do:
        - method: get
          url: url
          expect:
            - http_status_code: 200
            - valid_json
```

In the above example, we just specified `method`, `url` and `expect`. We didn't specify any `action`. That is because we have a hidden rule. If there is no action specified in the test case, we consider the action is `request` by default. And except `action` and `expect`, others will treat as parameters of `action`. 

So, in this case, the case will be translated to following Python code.

```python
response = request(method=get, url=url)
http_status_code(response, 200)
valid_json(response)
```


### Variables

You can define several variables and refer their values

```yaml
base_url = 'https://jsonplaceholder.typicode.com'
url = f'{base_url}/posts'
```

### Test Suite

For more information, please refer to test suites under `sample/`

## Command Line Usage

See `restest` help

```shell
$ restest -h
usage: restest [-h] [-e ENVIRONMENT] test_suite

positional arguments:
  test_suite            Test Suite File or Test Suite folder

optional arguments:
  -h, --help            show this help message and exit
  -e ENVIRONMENT, --environment ENVIRONMENT
                        Specify which environment to use
```

Run `restest` with a folder that contains test suite files in YAML

```shell
$ restest sample/
============================= test session starts ==============================
platform darwin -- Python 3.6.5, pytest-5.0.1, py-1.5.3, pluggy-0.12.0 -- /Users/user1/venv3/bin/python
cachedir: .pytest_cache
rootdir: /Users/user1/Development/Code/Github/restest
plugins: cov-2.5.1, allure-pytest-2.6.3
collected 6 items

sample/sdist/test_suite_00000_jsonplaceholder.py::test_list_all_posts PASSED
sample/sdist/test_suite_00000_jsonplaceholder.py::test_get_a_post_with_id_1 PASSED
sample/sdist/test_suite_00000_jsonplaceholder.py::test_create_a_post_with_userid_1 PASSED
sample/sdist/test_suite_00000_jsonplaceholder.py::test_pet_api_delete_success___http_201 PASSED
sample/sdist/test_suite_00001_jsonplaceholder_2.py::test_list_all_comment_of_post_1 PASSED
sample/sdist/test_suite_00002_simple.py::test_list_all_jsonplaceholder_posts PASSED

========================== 6 passed in 12.13 seconds ===========================
```

Run `restest` with a test suite file in YAML

```shell
$ restest sample/test-suite-00001-jsonplaceholder-2.yaml
/Users/user1/Code/Github/restest/sample/sdist/test_suite_00001_jsonplaceholder_2.py
================================= test session starts ==================================
platform darwin -- Python 3.7.3, pytest-4.6.3, py-1.8.0, pluggy-0.12.0 -- /Users/user1/Code/venv37/bin/python
cachedir: .pytest_cache
rootdir: /Users/user1/Code/Github/restest
plugins: cov-2.7.1
collected 1 item

sample/sdist/test_suite_00001_jsonplaceholder_2.py::test_list_all_comment_of_post_1 PASSED

============================== 1 passed in 36.87 seconds ===============================
```

## Development

```shell
$ python setup.py develop
running develop
running egg_info
writing restest.egg-info/PKG-INFO
writing dependency_links to restest.egg-info/dependency_links.txt
writing entry points to restest.egg-info/entry_points.txt
writing top-level names to restest.egg-info/top_level.txt
reading manifest file 'restest.egg-info/SOURCES.txt'
writing manifest file 'restest.egg-info/SOURCES.txt'
running build_ext
Creating /Users/user1/Code/venv37/lib/python3.7/site-packages/restest.egg-link (link to .)
Adding restest 0.0.1 to easy-install.pth file
Installing restest script to /Users/user1/Code/venv37/bin

Installed /Users/user1/Code/Github/restest
Processing dependencies for restest==0.0.1
Finished processing dependencies for restest==0.0.1
```
