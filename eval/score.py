#!/usr/bin/env python3
import json, subprocess, sys

def check_tests():
    try:
        result = subprocess.run(["python", "-m", "pytest", "tests/", "-q"],
                                capture_output=True, text=True, timeout=30)
        return 1.0 if result.returncode == 0 else 0.0
    except:
        return 0.0

def check_lint():
    try:
        result = subprocess.run(["python", "-m", "py_compile", "todo/cli.py"],
                                capture_output=True, text=True, timeout=10)
        return 1.0 if result.returncode == 0 else 0.0
    except:
        return 0.5

results = [
    {"name": "tests", "score": check_tests(), "weight": 0.7},
    {"name": "lint", "score": check_lint(), "weight": 0.3},
]
json.dump({"results": results}, sys.stdout)
