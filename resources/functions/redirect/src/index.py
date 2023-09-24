# Standard library imports
import os

# Local application / library specific imports
from .models.request import ApiGatewayRequest
from .controllers.redirect_controller import RedirectController

DDB_TABLE_NAME = os.environ["DDB_TABLE_NAME"]

redirect_controller = RedirectController(ddb_table_name=DDB_TABLE_NAME)


def event_handler(event, _context):
    # Reshape the request into a model
    request = ApiGatewayRequest.from_lambda_event(event)

    # Check if an alias exists for the domain, e.g. 'bss.com' for 'www.bss.com'.
    alias = redirect_controller.get_alias(request)

    # Decide which domain to retrieve a redirect for. If an alias is found, use it.
    # If no alias is found, use the domain in the original request.
    domain = alias.alias_domain if alias else request.domain

    # Retrieve the redirect location for the domain and path in the request.
    redirect_location = redirect_controller.get_redirect_location(
        domain=domain, request_path=request.path
    )

    # Add the resolved domain to the headers.
    base_headers = {"X-Resolved-Domain": domain}

    # If a redirect location is not found, return a 404.
    if not redirect_location:
        return {"statusCode": 404, "headers": base_headers}

    # Otherwise, return a 301 redirect to the location retreived from DynamoDB.
    # TODO: add query parameters to the redirect location.
    return {
        "statusCode": 301,
        "headers": base_headers | {"Location": redirect_location},
    }
