#!/usr/bin/env python
import pathlib
import argparse
import pytest
from parser import TestSuite, TestSuites

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--environment", default='qa', help="environment")
parser.add_argument("test_suite")
args = parser.parse_args()

ts_path = pathlib.Path(args.test_suite)
pytest_run = ''
print(ts_path)
print(ts_path.is_dir())
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