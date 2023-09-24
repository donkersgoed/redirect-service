"""The proxy module, responsible for the API Gateway proxy."""

from aws_cdk import (
    aws_apigateway as apigateway,
)
from constructs import Construct


class Proxy(Construct):
    """The proxy class, responsible for the API Gateway proxy."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Construct a new Proxy class."""
        super().__init__(scope, construct_id, **kwargs)

        self.rest_api = apigateway.RestApi(
            scope=self,
            id="ProxyApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
            deploy_options=apigateway.StageOptions(
                logging_level=apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
            ),
        )
