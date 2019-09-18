#!/usr/bin/env python

import argparse
import pytest
from parser import TestSuite

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--environment", default='qa', help="environment")
parser.add_argument("test_suite_file")
args = parser.parse_args()

ts = TestSuite(args.test_suite_file, env=args.environment)

ts.make()

outfile = ts.save()
pytest_args = f"-s -vv {outfile}"
pytest.main(pytest_args.split())