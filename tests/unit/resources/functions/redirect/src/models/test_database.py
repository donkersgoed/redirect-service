"""Test module for database models."""

# pylint: disable=import-outside-toplevel


class TestDatabase:
    """Test class for request models."""

    @staticmethod
    def test_alias_model():
        """Verify that the Alias model is correctly created from a DDB item."""
        from resources.functions.redirect.src.models.database import (
            Alias,
        )

        item = {
            "pk": "DomainAlias#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            "sk": "DomainAlias#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            "target_domain": "example.com",
        }

        model = Alias.from_ddb_item(item)
        assert model == Alias(
            source_domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            target_domain="example.com",
        )

    @staticmethod
    def test_get_redirect_model():
        """Verify that the RedirectOption model is correctly created from a DDB item."""
        from resources.functions.redirect.src.models.database import (
            RedirectOption,
        )

        item = {
            "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            "sk": "/",
            "target": "https://example.com",
        }

        model = RedirectOption.from_ddb_item(item)
        assert model == RedirectOption(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/",
            target="https://example.com",
        )

    @staticmethod
    def test_get_redirect_fallback_model():
        """Verify that the RedirectFallbackOption model is correctly created from a DDB item."""
        from resources.functions.redirect.src.models.database import (
            RedirectFallbackOption,
        )

        item = {
            "pk": "RedirectFallback#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            "sk": "/",
            "target": "https://example.com",
        }

        model = RedirectFallbackOption.from_ddb_item(item)
        assert model == RedirectFallbackOption(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/",
            target="https://example.com",
        )
