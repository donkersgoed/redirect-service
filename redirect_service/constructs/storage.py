"""The proxy module, responsible for all persistent storage."""

from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class Storage(Construct):
    """The proxy class, responsible for all persistent storage."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Construct a new Storage class."""
        super().__init__(scope, construct_id, **kwargs)

        self.ddb_table = dynamodb.Table(
            scope=self,
            id="RedirectsTable",
            partition_key=dynamodb.Attribute(
                name="pk", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
        )
