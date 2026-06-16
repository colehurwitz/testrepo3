#!/usr/bin/env python3
import json, subprocess, sys

def check_tests():
    try:
        result = subprocess.run(["python", "-m", "pytest", "tests/", "-q"],
                                capture_output=True, text=True, timeout=30)
        return {
            "name": "tests",
            "score": 1.0 if result.returncode == 0 else 0.0,
            "weight": 0.7,
            "passed": result.returncode == 0,
            "details": result.stdout.strip() or result.stderr.strip(),
        }
    except Exception as e:
        return {"name": "tests", "score": 0.0, "weight": 0.7, "passed": False, "details": str(e)}

def check_lint():
    try:
        result = subprocess.run(["python", "-m", "py_compile", "todo/cli.py"],
                                capture_output=True, text=True, timeout=10)
        return {
            "name": "lint",
            "score": 1.0 if result.returncode == 0 else 0.0,
            "weight": 0.3,
            "passed": result.returncode == 0,
            "details": "syntax ok" if result.returncode == 0 else result.stderr.strip(),
        }
    except Exception as e:
        return {"name": "lint", "score": 0.5, "weight": 0.3, "passed": False, "details": str(e)}

results = [check_tests(), check_lint()]
json.dump({"results": results}, sys.stdout)
