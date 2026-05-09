"""
Local test runner for the Lambda function.
Run this BEFORE deploying to AWS to verify your code works.

Usage:
    python test_local.py

No AWS account needed — this runs purely locally.
"""

import json
import sys
from lambda_function import lambda_handler


def run_test(test_name, event, expected_status=200):
    """Helper to call the Lambda handler and print results."""
    print(f"\n{'='*50}")
    print(f"Test: {test_name}")
    print(f"Input event: {json.dumps(event, indent=2)}")

    # Call the handler exactly like AWS would
    # We pass None for context since our function doesn't use it
    response = lambda_handler(event, None)

    status_code = response["statusCode"]
    body = json.loads(response["body"])

    print(f"\nResponse:")
    print(f"  Status Code : {status_code}")
    print(f"  Body        : {json.dumps(body, indent=4)}")

    # Assert the test passed
    assert status_code == expected_status, (
        f"FAIL: expected status {expected_status}, got {status_code}"
    )
    assert "message" in body, "FAIL: response body missing 'message' field"
    assert body["status"] == "success", f"FAIL: expected status=success, got {body['status']}"

    print(f"\n  PASSED")
    return body


def main():
    print("Testing Lambda function locally...\n")
    all_passed = True

    try:
        # --- Test 1: GET request with name in query string ---
        run_test(
            "GET /hello?name=Maruti",
            event={
                "httpMethod": "GET",
                "path": "/hello",
                "queryStringParameters": {"name": "Maruti"},
                "body": None,
            }
        )

        # --- Test 2: GET request with no name (should default to "World") ---
        body = run_test(
            "GET /hello (no name — defaults to World)",
            event={
                "httpMethod": "GET",
                "path": "/hello",
                "queryStringParameters": None,
                "body": None,
            }
        )
        assert "World" in body["message"], "FAIL: should say 'World' when no name given"

        # --- Test 3: POST request with JSON body ---
        run_test(
            "POST /hello  body={name: Lambda Learner}",
            event={
                "httpMethod": "POST",
                "path": "/hello",
                "queryStringParameters": None,
                "body": json.dumps({"name": "Lambda Learner"}),
            }
        )

        # --- Test 4: Load from test_event.json ---
        with open("test_event.json") as f:
            file_event = json.load(f)
            # Remove the _comment key (not a real event field)
            file_event.pop("_comment", None)

        run_test("Event loaded from test_event.json", file_event)

    except AssertionError as e:
        print(f"\n  {e}")
        all_passed = False
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        all_passed = False

    print(f"\n{'='*50}")
    if all_passed:
        print("All tests passed! Your Lambda is ready to deploy.")
        sys.exit(0)
    else:
        print("Some tests failed. Fix the issues above before deploying.")
        sys.exit(1)


if __name__ == "__main__":
    main()
