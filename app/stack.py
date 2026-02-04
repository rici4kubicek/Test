import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
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
            description="Lambda function to fetch EUR/CZK and USD/CZK exchange rates from CNB",
            timeout=cdk.Duration.seconds(30),
            memory_size=128,
        )

        # Create EventBridge rule to trigger Lambda daily at 16:00 UTC
        # Cron expression: 0 16 * * ? *  (16:00 UTC every day)
        rule = events.Rule(
            self,
            "DailyExchangeRateRule",
            schedule=events.Schedule.cron(
                hour="16",
                minute="0",
                day="*",
                month="*",
                week_day="*",
            ),
            description="Trigger exchange rate Lambda function daily at 16:00 UTC",
        )

        # Add Lambda function as target
        rule.add_target(targets.LambdaFunction(lambda_function))

        # Output the function name
        cdk.CfnOutput(
            self,
            "LambdaFunctionName",
            value=lambda_function.function_name,
            description="Name of the Lambda function",
            export_name="LambdaFunctionName",
        )

        # Output the EventBridge rule
        cdk.CfnOutput(
            self,
            "EventBridgeRuleName",
            value=rule.rule_name,
            description="Name of the EventBridge rule",
            export_name="EventBridgeRuleName",
        )
