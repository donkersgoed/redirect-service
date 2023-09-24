# Standard library imports
from unittest.mock import MagicMock

# Local application / library specific imports
from resources.functions.redirect.src.models.request import ApiGatewayRequest
from resources.functions.redirect.src.models.database import Alias


class TestRedirectController:
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

    # @staticmethod
    # def test_get_alias_found() -> None:
    #     """Test that get_alias returns an Alias object when it exists in the database."""
    #     # 1. ARRANGE
    #     from resources.functions.redirect.src.controllers.redirect_controller import (
    #         RedirectController,
    #     )

    #     controller = RedirectController(ddb_table_name="mock_table")
    #     controller._ddb_table.query = MagicMock(
    #         return_value={
    #             "Items": [],
    #             "Count": 0,
    #             "ScannedCount": 0,
    #             "ResponseMetadata": {
    #                 # Stripped
    #             },
    #         }
    #     )

    #     request = ApiGatewayRequest(
    #         domain="mock_domain", path="/mock_path", query_params=None
    #     )

    #     # 2. ACT
    #     response = controller.get_alias(request)

    #     # 3. ASSERT
    #     assert response is Alias(alias_domain="example.com")

    @staticmethod
    def test_get_redirect_location_no_match_found() -> None:
        """Test that get_redirect_location returns None when no match is found."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [],
                "Count": 0,
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
        assert response is None

    @staticmethod
    def test_get_redirect_location_exact_match_found() -> None:
        """Test that get_redirect_location returns a redirect location when an exact match is found."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com",
                        "type": "EXACT",
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
    def test_get_redirect_location_multiple_found_including_exact() -> None:
        """Test that get_redirect_location returns the exact match when multiple results are found."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1",
                        "target": "https://example.com/begins_with",
                        "type": "BEGINS_WITH",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/",
                        "target": "https://example.com/exact/",
                        "type": "EXACT",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 3,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path1/",
        )

        # 3. ASSERT
        assert response == "https://example.com/exact/"

    @staticmethod
    def test_get_redirect_location_multiple_exact_priority() -> None:
        """Test that get_redirect_location returns the exact match first."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/",
                        "target": "https://example.com/begins_with",
                        "type": "BEGINS_WITH",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/",
                        "target": "https://example.com/exact/",
                        "type": "EXACT",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 3,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path1/",
        )

        # 3. ASSERT
        assert response == "https://example.com/exact/"

    @staticmethod
    def test_get_redirect_location_begins_with() -> None:
        """Test that get_redirect_location returns the begins_with if there are no exact matches."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/",
                        "target": "https://example.com/exact/",
                        "type": "EXACT",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com/begins_with/",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 3,
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
        assert response == "https://example.com/begins_with/"

    @staticmethod
    def test_get_redirect_location_multiple_begins_with() -> None:
        """Test that get_redirect_location returns the begins_with with the most matching characters."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/subpath1",
                        "target": "https://example.com/option1/",
                        "type": "BEGINS_WITH",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/",
                        "target": "https://example.com/option2/",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 3,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path1/subpath1",
        )

        # 3. ASSERT
        assert response == "https://example.com/option1/"

    @staticmethod
    def test_get_redirect_location_multiple_begins_with_reverse_order() -> None:
        """Test that get_redirect_location returns the begins_with with the most matching characters."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/",
                        "target": "https://example.com/option2/",
                        "type": "BEGINS_WITH",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path1/subpath1",
                        "target": "https://example.com/option1/",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 3,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path1/subpath1",
        )

        # 3. ASSERT
        assert response == "https://example.com/option1/"

    @staticmethod
    def test_get_redirect_location_no_match() -> None:
        """Test that get_redirect_location returns the best matching begins_with option."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path2",
                        "target": "https://example.com/option1/",
                        "type": "BEGINS_WITH",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com/option2/",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 3,
                "ScannedCount": 3,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path2/something",
        )

        # 3. ASSERT
        assert response == "https://example.com/option1/"

    @staticmethod
    def test_get_redirect_location_no_match_root_fallback() -> None:
        """Test that get_redirect_location returns the best matching begins_with option, which is the root."""
        # 1. ARRANGE
        from resources.functions.redirect.src.controllers.redirect_controller import (
            RedirectController,
        )

        controller = RedirectController(ddb_table_name="mock_table")
        controller._ddb_table.query = MagicMock(
            return_value={
                "Items": [
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/path2",
                        "target": "https://example.com/option1/",
                        "type": "BEGINS_WITH",
                    },
                    {
                        "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                        "sk": "/",
                        "target": "https://example.com/option2/",
                        "type": "BEGINS_WITH",
                    },
                ],
                "Count": 2,
                "ScannedCount": 2,
                "ResponseMetadata": {
                    # Stripped
                },
            }
        )

        # 2. ACT
        response = controller.get_redirect_location(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            request_path="/path3/something",
        )

        # 3. ASSERT
        assert response == "https://example.com/option2/"
