# restest

Simple RESTFul API Test Framework for learning, reinventing wheels (don't do it)

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

## Usage

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
