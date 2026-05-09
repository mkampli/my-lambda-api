"""
AWS Lambda Hello World API
Handler: lambda_function.lambda_handler

Supports:
  GET  /hello?name=YourName
  POST /hello  body: {"name": "YourName"}
"""

import json
from datetime import datetime, timezone


def lambda_handler(event, context):
    """
    Main Lambda entry point. AWS calls this function with an 'event'
    dict describing the incoming request, and a 'context' object with
    runtime information (we won't use context in this example).
    """
    print("Received event:", json.dumps(event))  # Logged to CloudWatch

    try:
        # --- Extract the caller's name ---
        name = extract_name(event)

        # --- Build the response body ---
        body = {
            "message": f"Hello, {name}! Welcome to AWS Lambda.",
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method", "UNKNOWN"),
        }

        return build_response(200, body)

    except Exception as e:
        print(f"Error: {e}")
        return build_response(500, {"message": "Internal server error", "status": "error"})


def extract_name(event):
    """
    Try multiple places a name might come from:
    1. Query string: GET /hello?name=Maruti
    2. JSON body:    POST /hello  {"name": "Maruti"}
    3. Default to "World" if not found
    """
    # Check query string parameters (GET requests)
    query_params = event.get("queryStringParameters") or {}
    if query_params.get("name"):
        return query_params["name"]

    # Check JSON body (POST requests)
    body = event.get("body")
    if body:
        try:
            # Body may be a string (from API Gateway) or already a dict (local test)
            if isinstance(body, str):
                body = json.loads(body)
            if isinstance(body, dict) and body.get("name"):
                return body["name"]
        except json.JSONDecodeError:
            pass  # Body wasn't JSON — that's fine

    return "World"


def build_response(status_code, body):
    """
    Return a properly formatted API Gateway response.
    The 'headers' and 'statusCode' keys are required by API Gateway.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",   # Allow browser requests (CORS)
        },
        "body": json.dumps(body),
    }
