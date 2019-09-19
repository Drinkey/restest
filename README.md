# restest
Simple RESTFul API Test Framework for learning, reinventing wheels (don't do it)

# Environment

Python 3.6.5
Python 3.7

# Usage


```
$ python src/restest.py sample/
============================= test session starts ==============================
platform darwin -- Python 3.6.5, pytest-5.0.1, py-1.5.3, pluggy-0.12.0 -- /Users/jkzhang/venv3/bin/python
cachedir: .pytest_cache
rootdir: /Users/jkzhang/Development/Code/Github/restest
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

# Extending functions

