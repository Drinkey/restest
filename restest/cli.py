#!/usr/bin/env python
import pathlib
import argparse
import pytest
from restest.parser import TestSuite, TestSuites

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--environment",
        default='qa',
        help="Specify which environment to use"
    )
    parser.add_argument(
        "test_suite",
        help="Test Suite File or Test Suite folder"
    )
    args = parser.parse_args()
    ts_path = pathlib.Path(args.test_suite)
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

if __name__ == "__main__":
    main()
