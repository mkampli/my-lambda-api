# My Lambda API

A serverless Hello World REST API built with AWS Lambda, Python, API Gateway, and WAF.

## Quick Start

### 1. Test locally
```bash
python test_local.py
```

### 2. Deploy manually (first time only)
```bash
zip function.zip lambda_function.py
aws lambda create-function \
  --function-name hello-world-api \
  --runtime python3.12 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-basic-execution \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

### 3. After that — just push to deploy
```bash
git push origin main
# GitHub Actions handles the rest!
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/hello?name=YourName` | Returns a greeting |
| POST | `/hello` | Body: `{"name": "YourName"}` |

## Full Setup Guide

See `AWS_Lambda_Learning_Guide.md` for step-by-step instructions covering:
- AWS CLI setup
- IAM user creation
- API Gateway configuration
- WAF setup
# My Lambda API
