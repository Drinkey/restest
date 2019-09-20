#!/usr/bin/env python
import pathlib
import pytest
from parser import TestSuite, TestSuites

def main(args):
    ts_path = pathlib.Path(args.test_suite)
    print(ts_path)
    print(ts_path.is_dir())
    pytest_run = ''
    if ts_path.is_file():
        ts = TestSuite(args.test_suite, env=args.environment)
        ts.make()
        pytest_run = ts.save()

    elif ts_path.is_dir():
        ts = TestSuites(args.test_suite, env=args.environment)
        pytest_run = ts.collect()

    print(pytest_run)
    pytest_args = f"-s -vv {pytest_run}"
    pytest.main(pytest_args.split())