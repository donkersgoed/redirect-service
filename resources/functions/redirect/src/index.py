"""The redirect Lambda Function, responsible for redirecting requests."""

# Standard library imports
import os
from urllib.parse import urlencode

# Local application / library specific imports
from .models.request import ApiGatewayRequest
from .controllers.redirect_controller import RedirectController

DDB_TABLE_NAME = os.environ["DDB_TABLE_NAME"]

redirect_controller = RedirectController(ddb_table_name=DDB_TABLE_NAME)


def event_handler(event, _context):
    """
    Handle an incoming request from API Gateway.

    The function returns a 404 if no redirect option is found, or a 301
    with a 'Location' header if it is.
    """
    # Reshape the request into a model
    request = ApiGatewayRequest.from_lambda_event(event)

    # Check if an alias exists for the domain, e.g. 'bss.com' for 'www.bss.com'.
    alias = redirect_controller.get_alias(request)

    # Decide which domain to retrieve a redirect for. If an alias is found, use it.
    # If no alias is found, use the domain in the original request.
    domain = alias.target_domain if alias else request.domain

    # Retrieve the redirect location for the domain and path in the request.
    redirect_location = redirect_controller.get_redirect_location(
        domain=domain, request_path=request.path
    )

    # Add the resolved domain to the headers.
    base_headers = {"X-Resolved-Domain": domain}

    # If a redirect location is not found, return a 404.
    if not redirect_location:
        return {"statusCode": 404, "headers": base_headers}

    # A redirect location is found, so we add any query parameters
    # from the original request to the redirect location.
    if request.query_params:
        redirect_location += "?" + urlencode(request.query_params)

    # Return a 301 redirect to the location retreived from DynamoDB.
    return {
        "statusCode": 301,
        "headers": base_headers | {"Location": redirect_location},
    }
