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
            "ExchangeRateFetcher",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset(os.path.join(os.path.dirname(__file__), "../lambda")),
            description="Fetches current EUR/CZK and USD/CZK exchange rates from CNB",
            timeout=cdk.Duration.seconds(30),
            memory_size=128,
        )

        # Create EventBridge rule to trigger Lambda daily at 16:00 UTC
        # Cron expression: 0 16 * * ? *  (16:00 UTC every day)
        rule = events.Rule(
            self,
            "DailyExchangeRateTrigger",
            schedule=events.Schedule.cron(
                hour="16",
                minute="0",
                day="*",
                month="*",
                week_day="*",
            ),
            description="Daily trigger for CNB exchange rate fetcher at 16:00 UTC",
        )

        # Add Lambda function as target
        rule.add_target(targets.LambdaFunction(lambda_function))

        # Output the function name
        cdk.CfnOutput(
            self,
            "ExchangeRateFetcherArn",
            value=lambda_function.function_arn,
            description="ARN of the ExchangeRateFetcher Lambda function",
            export_name="ExchangeRateFetcherArn",
        )

        # Output the EventBridge rule
        cdk.CfnOutput(
            self,
            "DailyExchangeRateTriggerName",
            value=rule.rule_name,
            description="Name of the daily exchange rate trigger rule",
            export_name="DailyExchangeRateTriggerName",
        )
