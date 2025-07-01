import subprocess
import sys
import os

SCRIPT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "main.py"))
CSV = os.path.join(os.path.dirname(__file__), "..", "products.csv")


def run_script(args):
    result = subprocess.run(
        [sys.executable, SCRIPT] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )
    return result.stdout


def test_filter_greater_than():
    output = run_script(["--file", CSV, "--where", "price>1000"])
    assert "galaxy s23 ultra" in output
    assert "iphone 15 pro" not in output


def test_filter_less_than():
    output = run_script(["--file", CSV, "--where", "price<200"])
    assert "redmi note 12" in output
    assert "galaxy s23 ultra" not in output


def test_filter_equal_number():
    output = run_script(["--file", CSV, "--where", "price=999"])
    assert "iphone 15 pro" in output
    assert "galaxy z flip 5" in output
    assert "galaxy s23 ultra" not in output


def test_filter_float_number():
    output = run_script(["--file", CSV, "--where", "rating>4.7"])
    assert "galaxy s23 ultra" in output
    assert "iphone 15 pro" in output
    assert "iphone 14" not in output


def test_filter_equal_text():
    output = run_script(["--file", CSV, "--where", "brand=apple"])
    assert "iphone 15 pro" in output
    assert "iphone 14" in output
    assert "iphone se" in output
    assert "galaxy s23 ultra" not in output
    assert "redmi note 12" not in output
    assert "poco x5 pro" not in output


def test_aggregate_avg():
    output = run_script(["--file", CSV, "--aggregate", "price=avg"])
    assert "avg" in output
    assert "error" not in output.lower()


def test_aggregate_min():
    output = run_script(["--file", CSV, "--aggregate", "price=min"])
    assert "min" in output
    assert "149" in output


def test_aggregate_max():
    output = run_script(["--file", CSV, "--aggregate", "price=max"])
    assert "max" in output
    assert "1199" in output


def test_no_results_filter():
    output = run_script(["--file", CSV, "--where", "price>5000"])
    assert "No rows found." in output


def test_str_in_filter():
    output = run_script(["--file", CSV, "--where", "brand>apple"])
    assert "iphone 15 pro" not in output
    assert "iphone 14" not in output
    assert "iphone se" not in output


def test_invalid_aggregate_operation_1():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--file", CSV, "--aggregate", "price=invalid"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    assert "Invalid operation" in result.stderr


def test_invalid_aggregate_operation_2():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--file", CSV, "--aggregate", "price!avg"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    assert "Invalid aggregate condition. Use =" in result.stderr


def test_invalid_where_condition():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--file", CSV, "--where", "price!500"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    assert "Invalid" in result.stderr


def test_no_file_provided():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    assert "error" in result.stderr.lower()
    assert "required" in result.stderr.lower()


def test_file_not_found():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--file", "non_existent_file.csv"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    assert "File non_existent_file.csv not found." in result.stderr
