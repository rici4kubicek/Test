import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
import os


class LambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Lambda function
        lambda_function = lambda_.Function(
            self,
            "HelloWorldFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset(os.path.join(os.path.dirname(__file__), "../lambda")),
            description="A simple Lambda function",
            timeout=cdk.Duration.seconds(30),
            memory_size=128,
        )

        # Output the function name
        cdk.CfnOutput(
            self,
            "LambdaFunctionName",
            value=lambda_function.function_name,
            description="Name of the Lambda function",
            export_name="LambdaFunctionName",
        )
