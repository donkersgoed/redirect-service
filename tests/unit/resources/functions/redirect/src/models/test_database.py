class TestRequest:
    @staticmethod
    def test_get_model_exact():
        from resources.functions.redirect.src.models.database import (
            RedirectOption,
            RedirectType,
        )

        item = {
            "sk": "/",
            "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            "target": "https://example.com",
            "type": "EXACT",
        }

        model = RedirectOption.from_ddb_item(item)
        assert model == RedirectOption(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/",
            target="https://example.com",
            type=RedirectType.EXACT,
        )

    @staticmethod
    def test_get_model_begins_with():
        from resources.functions.redirect.src.models.database import (
            RedirectOption,
            RedirectType,
        )

        item = {
            "sk": "/",
            "pk": "Redirect#j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            "target": "https://example.com",
            "type": "BEGINS_WITH",
        }

        model = RedirectOption.from_ddb_item(item)
        assert model == RedirectOption(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/",
            target="https://example.com",
            type=RedirectType.BEGINS_WITH,
        )
