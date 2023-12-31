"""Module for request models."""

# Standard library imports
from dataclasses import dataclass
from typing import Optional

# Local application / library specific imports
from . import BaseDataclass


@dataclass
class ApiGatewayRequest(BaseDataclass):
    """The ApiGatewayRequest model, representing an API Gateway request."""

    domain: str
    path: str
    query_params: Optional[dict]

    @classmethod
    def from_lambda_event(cls, event: dict) -> "ApiGatewayRequest":
        """Convert a Lambda event to a ApiGatewayRequest model."""
        return cls(
            domain=event["requestContext"]["domainName"],
            path=event["path"],
            query_params=event["queryStringParameters"],
        )
