"""Test module for the redirect controller."""

# pylint: disable=import-outside-toplevel, protected-access

# Standard library imports
from unittest.mock import MagicMock

# Local application / library specific imports
from resources.functions.redirect.src.models.request import ApiGatewayRequest
from resources.functions.redirect.src.models.database import Alias


class TestRedirectController:
    """Testclass for the redirect controller."""

    @staticmethod
    def test_get_alias_not_found() -> None:
        """Test that get_alias returns None when no alias exists in the database."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [],
                "Count": 0,
                "ScannedCount": 0,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        request = ApiGatewayRequest(
            domain="mock_domain", path="/mock_path", query_params=None
        )

        # 2. ACT
        response = controller.get_alias(request)

        # 3. ASSERT
        assert response is None

    @staticmethod
    def test_get_alias_found() -> None:
        """Test that get_alias returns an Alias object when it exists in the database."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "DomainAlias#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "DomainAlias#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "target_domain": "example.com",
                    }
                ],
                "Count": 1,
                "ScannedCount": 1,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        request = ApiGatewayRequest(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/mock_path",
            query_params=None,
        )

        # 2. ACT
        response = controller.get_alias(request)

        # 3. ASSERT
        assert response == Alias(
            source_domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            target_domain="example.com",
        )

    @staticmethod
    def test_get_redirect_location_exact_match_found() -> None:
        """Test that get_redirect_location returns a location when an exact match is found."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._get_redirect_from_ddb = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com",
                    }
                ],
                "Count": 1,
                "ScannedCount": 1,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com", request_path="/"
        )

        # 3. ASSERT
        assert response == "https://example.com"

    @staticmethod
    def test_get_redirect_location_no_fallback_location() -> None:
        """Verify that get_redirect_location() returns None when no matches are found."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._get_redirect_from_ddb = MagicMock(
            return_value={
                "Items": [],
                "Count": 0,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )
        controller._get_redirect_fallbacks_from_ddb = MagicMock(
            return_value={
                "Items": [],
                "Count": 0,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/",
        )

        # 3. ASSERT
        assert response is None

    @staticmethod
    def test_get_redirect_location_one_fallback_location() -> None:
        """Verify that get_redirect_location() returns a fallback location when it exists."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._get_redirect_from_ddb = MagicMock(
            return_value={
                "Items": [],
                "Count": 0,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )
        controller._get_redirect_fallbacks_from_ddb = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "RedirectFallback#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1",
                        "target": "https://example.com/path1",
                    }
                ],
                "Count": 1,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path1/2",
        )

        # 3. ASSERT
        assert response == "https://example.com/path1"

    @staticmethod
    def test_get_redirect_location_multiple_fallback_locations() -> None:
        """Verify that get_redirect_location() returns the best fallback location."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._get_redirect_from_ddb = MagicMock(
            return_value={
                "Items": [],
                "Count": 0,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )
        controller._get_redirect_fallbacks_from_ddb = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "RedirectFallback#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1",
                        "target": "https://example.com/option1",
                    },
                    {
                        "pk": "RedirectFallback#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com/option2",
                    },
                ],
                "Count": 2,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path1/2",
        )

        # 3. ASSERT
        assert response == "https://example.com/option1"
