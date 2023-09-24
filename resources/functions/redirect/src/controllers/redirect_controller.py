# Standard library imports
from typing import Optional, List

# Related third party imports
import boto3
from boto3.dynamodb.conditions import Key


# Local application / library specific imports
from ..models.request import ApiGatewayRequest
from ..models.database import Alias, RedirectOption, RedirectType


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
        print(response)
        if response["Count"] == 0:
            return None
        return Alias.from_ddb_item(response["Items"][0])

    def get_redirect_location(self, domain: str, request_path: str) -> Optional[str]:
        """Get the best redirect location from the database, or None if no options are found."""
        pk = f"Redirect#{domain}"
        sk = request_path

        response = self._ddb_table.query(
            KeyConditionExpression=Key("pk").eq(pk) & Key("sk").begins_with(sk),
        )

        # Reshape the DDB responses into models
        redirects: List[RedirectOption] = []
        for item in response["Items"]:
            redirects.append(RedirectOption.from_ddb_item(item))

        # Loop over all redirects, return an exact match if it is found,
        # or track which "BEGINS_WITH" redirect option has the most matching characters.
        best_match = None
        max_matching_characters = 0
        for redirect in redirects:
            if self._exact_match_or_none(request_path, redirect):
                return redirect.target

            if redirect.type == RedirectType.BEGINS_WITH:
                matching_characters = len(redirect.path)
                if matching_characters > max_matching_characters:
                    best_match = redirect
                    max_matching_characters = matching_characters

        return best_match.target if best_match else None

    def _exact_match_or_none(
        self, request_path: str, redirect_option: RedirectOption
    ) -> Optional[RedirectOption]:
        """Check if the match type is exact and return the redirect option if the request path exactly matches."""
        if redirect_option.type == RedirectType.EXACT:
            # The redirect option requires an exact match.
            # Return the RedirectOption if the match is successful.
            # Otherwise, return None.
            return (
                redirect_option
                if redirect_option.path.lower() == request_path.lower()
                else None
            )
