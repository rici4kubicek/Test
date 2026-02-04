# AWS CDK Lambda Project

This is an AWS CDK project in Python that deploys a simple Lambda function.

## Prerequisites

- Python 3.9 or later
- AWS CLI configured with appropriate credentials
- AWS CDK CLI: `npm install -g aws-cdk`

## Project Structure

```
├── app/
│   ├── __main__.py     # CDK app entry point
│   └── stack.py        # CDK Stack definition
├── lambda/
│   └── index.py        # Lambda function code
├── requirements-dev.txt # Python CDK dependencies
├── cdk.json           # CDK configuration
└── .gitignore         # Git ignore rules
```

## Installation

1. Create a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Install AWS CDK CLI globally:
```bash
npm install -g aws-cdk
```

## Deployment

First, bootstrap the AWS environment (required once per account/region):

```bash
cdk bootstrap
```

Deploy the stack:

```bash
cdk deploy
```

## Useful Commands

- `cdk synth` - Emits the synthesized CloudFormation template
- `cdk deploy` - Deploy the stack to AWS
- `cdk diff` - Compare deployed stack with current state
- `cdk destroy` - Destroy the deployed stack
- `cdk ls` - List all stacks in the app

## Configuration

Edit the Lambda function code in `lambda/index.py` to customize the function behavior.

Modify `app/stack.py` to add additional AWS resources or configure the Lambda function (e.g., environment variables, IAM roles, etc.).