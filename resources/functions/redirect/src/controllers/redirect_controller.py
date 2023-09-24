# Standard library imports
from typing import Optional, List

# Related third party imports
import boto3
from boto3.dynamodb.conditions import Key


# Local application / library specific imports
from ..models.request import ApiGatewayRequest
from ..models.database import Alias, RedirectOption, RedirectFallbackOption


class RedirectController:
    def __init__(self, ddb_table_name: str) -> None:
        """Construct a new RedirectController."""
        dynamodb = boto3.resource("dynamodb")
        self._ddb_table = dynamodb.Table(ddb_table_name)

    def get_alias(self, request: ApiGatewayRequest) -> Optional[Alias]:
        """Return an Alias object from DDB or None if no alias exists."""
        key = f"DomainAlias#{request.domain}"
        response = self._ddb_table.query(
            KeyConditionExpression=Key("pk").eq(key) & Key("sk").eq(key),
        )

        if response["Count"] == 0:
            return None

        return Alias.from_ddb_item(response["Items"][0])

    def get_redirect_location(self, domain: str, request_path: str) -> Optional[str]:
        """
        Get the best redirect location from the database, or None if no options are found.

        This function first checks for exact domain and path matches, and returns them if they are found.
        If none are found, it will look for fallback redirects, where the path in the database partially
        matches the request. If any are found, the best match is returned. If none are found,
        None is returned.
        """

        ddb_response = self._get_redirect_from_ddb(domain, request_path)

        if ddb_response["Count"] == 1:
            return ddb_response["Items"][0]["target"]

        if ddb_response["Count"] == 0:
            return self._get_fallback_redirect_location(domain, request_path)

    def _get_fallback_redirect_location(
        self, domain: str, request_path: str
    ) -> Optional[str]:
        """Return the best fallback redirect location for the given request path, or None."""
        ddb_response = self._get_redirect_fallbacks_from_ddb(domain=domain)

        # Reshape the DDB responses into models
        redirect_options: List[RedirectFallbackOption] = []
        for item in ddb_response["Items"]:
            redirect_options.append(RedirectFallbackOption.from_ddb_item(item))

        # Loop over all redirects, return an exact match if it is found,
        # or track which "BEGINS_WITH" redirect option has the most matching characters.
        best_match = None
        max_matching_characters = 0
        for redirect in redirect_options:
            if redirect.path in request_path:
                matching_characters = len(redirect.path)
                if matching_characters > max_matching_characters:
                    best_match = redirect
                    max_matching_characters = matching_characters

        return best_match.target if best_match else None

    def _get_redirect_from_ddb(self, domain: str, request_path: str):
        """
        Extracted DDB redirect request for easy mocking.

        Queries the database for all exactly matching redirect locations
        for the requested path.
        """
        response = self._ddb_table.query(
            KeyConditionExpression=Key("pk").eq(f"Redirect#{domain}")
            & Key("sk").eq(request_path),
        )

        if response["Count"] > 1 or len(response["Items"]) > 1:
            raise Exception("Multiple redirect options found for request path")

        return response

    def _get_redirect_fallbacks_from_ddb(self, domain: str):
        """Extracted DDB redirect fallbacks request for easy mocking."""
        return self._ddb_table.query(
            KeyConditionExpression=Key("pk").eq(f"RedirectFallback#{domain}"),
        )
