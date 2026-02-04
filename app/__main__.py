#!/usr/bin/env python3
import aws_cdk as cdk
from stack import LambdaStack

app = cdk.App()

LambdaStack(
    app,
    "LambdaStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region"),
    ),
)

app.synth()
