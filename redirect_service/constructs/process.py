from aws_cdk import (
    Duration,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
)
from constructs import Construct


class Process(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        proxy_api: apigateway.RestApi,
        ddb_table: dynamodb.Table,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        redirect_handler = lambda_.Function(
            scope=self,
            id="RedirectHandler",
            code=lambda_.Code.from_asset("resources/functions/redirect/"),
            handler="src.index.event_handler",
            architecture=lambda_.Architecture.ARM_64,
            runtime=lambda_.Runtime.PYTHON_3_11,
            timeout=Duration.seconds(1),
            memory_size=1024,
            environment={"DDB_TABLE_NAME": ddb_table.table_name},
        )

        # Use an alias to allow API Gateway to gracefully switch between versions
        lambda_alias = lambda_.Alias(
            scope=self,
            id="RedirectHandlerLiveAlias",
            alias_name="live",
            version=redirect_handler.current_version,
        )
        ddb_table.grant_read_data(lambda_alias)

        redirect_integration = apigateway.LambdaIntegration(
            handler=lambda_alias, allow_test_invoke=False
        )

        # Route all GET requests to the Lambda Function
        proxy_resource = proxy_api.root.add_proxy(
            any_method=False,
            default_integration=redirect_integration,
        )
        proxy_resource.add_method("GET", redirect_integration)
