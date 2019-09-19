import pathlib
import pytest
import parser
import code

TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent.parent

def test_parse_testsuite_0000_sample():
    sample = f"{TEMPLATE_DIR}/sample/test-suite-00000-jsonplaceholder.yaml"
    ret = parser.yaml2dict(sample)
    print(ret)

def test_test_suite_parse_init_one_param_no_exception():
    sample = f"{TEMPLATE_DIR}/sample/test-suite-00000-jsonplaceholder.yaml"
    ts = parser.TestSuite(test_suite_file=sample)
    ts.make()
    print(ts.code)

def test_test_case_make():
    codeobj = code.PytestCodeBuilder()
    testcase = {
                    'name': 'Create post Success - HTTP 201', 
                    'do': [
                        {
                            'action': 'request',
                            'method': 'post', 
                            'data': 'ds_file_exception_code_201',
                            'expect': 
                            [
                                {'http_status_code': 201}, 
                                'valid_json', 
                                {'contains_text': ['create success', 'id=2000']}
                            ]
                        }
                    ]
    }
    tc = parser.TestCase(testcase, codeobj)
    tc.make()
    print(tc.code)
    assert 'def test_create_post' in str(tc.code)
    assert 'http_status_code(response, 201)' in str(tc.code)

def test_test_suites_discover():
    sample = f"{TEMPLATE_DIR}/sample"
    tsf = parser.TestSuites(sample)
    all_tc = tsf.discover()
    print(all_tc)