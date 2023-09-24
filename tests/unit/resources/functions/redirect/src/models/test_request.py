"""Test module for request models."""

# pylint: disable=import-outside-toplevel


class TestRequest:
    """Test class for the request models."""

    @staticmethod
    def test_get_model_no_path_no_params():
        """Verify that a request with a simple path and no query params is stored correctly."""
        from resources.functions.redirect.src.models.request import ApiGatewayRequest

        request = {
            "resource": "/",
            "path": "/",
            "httpMethod": "GET",
            "headers": {
                # Stripped
            },
            "multiValueHeaders": {
                # Stripped
            },
            "queryStringParameters": None,
            "multiValueQueryStringParameters": None,
            "pathParameters": None,
            "stageVariables": None,
            "requestContext": {
                "resourceId": "5nwv43a8w7",
                "resourcePath": "/",
                "httpMethod": "GET",
                "extendedRequestId": "LtOBPHySDoEFn7Q=",
                "requestTime": "23/Sep/2023:10:53:21 +0000",
                "path": "/prod",
                "accountId": "739178438747",
                "protocol": "HTTP/1.1",
                "stage": "prod",
                "domainPrefix": "j3qfzmnyjl",
                "requestTimeEpoch": 1695466401265,
                "requestId": "04b3ff13-6ad1-44fa-bbe7-def19b601573",
                "identity": {},
                "domainName": "j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                "apiId": "j3qfzmnyjl",
            },
            "body": None,
            "isBase64Encoded": False,
        }

        model = ApiGatewayRequest.from_lambda_event(request)
        assert model == ApiGatewayRequest(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/",
            query_params=None,
        )

    @staticmethod
    def test_get_model_path_no_params():
        """Verify that a request with a path but no query parameters is stored correctly."""
        from resources.functions.redirect.src.models.request import ApiGatewayRequest

        request = {
            "resource": "/{proxy+}",
            "path": "/test/1/bites-1",
            "httpMethod": "GET",
            "headers": {
                # Stripped
            },
            "multiValueHeaders": {
                # Stripped
            },
            "queryStringParameters": None,
            "multiValueQueryStringParameters": None,
            "pathParameters": None,
            "stageVariables": None,
            "requestContext": {
                "resourceId": "6dw8bq",
                "resourcePath": "/{proxy+}",
                "httpMethod": "GET",
                "extendedRequestId": "LtMfNH7NDoEFqOQ=",
                "requestTime": "23/Sep/2023:10:42:53 +0000",
                "path": "/prod/test/1/bites-1",
                "accountId": "739178438747",
                "protocol": "HTTP/1.1",
                "stage": "prod",
                "domainPrefix": "j3qfzmnyjl",
                "requestTimeEpoch": 1695465773882,
                "requestId": "fcc0e09d-ee18-4483-a33b-47321e82900e",
                "identity": {
                    # Stripped
                },
                "domainName": "j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                "apiId": "j3qfzmnyjl",
            },
            "body": None,
            "isBase64Encoded": False,
        }

        model = ApiGatewayRequest.from_lambda_event(request)
        assert model == ApiGatewayRequest(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/test/1/bites-1",
            query_params=None,
        )

    @staticmethod
    def test_get_model_path_params():
        """Verify that a request with a complex path and query parameters is stored correctly."""
        from resources.functions.redirect.src.models.request import ApiGatewayRequest

        request = {
            "resource": "/{proxy+}",
            "path": "/test/1/bites-1",
            "httpMethod": "GET",
            "headers": {
                # Stripped
            },
            "multiValueHeaders": {
                # Stripped
            },
            "queryStringParameters": {"some_param": "12"},
            "multiValueQueryStringParameters": {"some_param": ["12"]},
            "pathParameters": None,
            "stageVariables": None,
            "requestContext": {
                "resourceId": "6dw8bq",
                "resourcePath": "/{proxy+}",
                "httpMethod": "GET",
                "extendedRequestId": "LtMfNH7NDoEFqOQ=",
                "requestTime": "23/Sep/2023:10:42:53 +0000",
                "path": "/prod/test/1/bites-1",
                "accountId": "739178438747",
                "protocol": "HTTP/1.1",
                "stage": "prod",
                "domainPrefix": "j3qfzmnyjl",
                "requestTimeEpoch": 1695465773882,
                "requestId": "fcc0e09d-ee18-4483-a33b-47321e82900e",
                "identity": {
                    # Stripped
                },
                "domainName": "j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
                "apiId": "j3qfzmnyjl",
            },
            "body": None,
            "isBase64Encoded": False,
        }

        model = ApiGatewayRequest.from_lambda_event(request)
        assert model == ApiGatewayRequest(
            domain="j3qfzmnyjl.execute-api.eu-west-1.amazonaws.com",
            path="/test/1/bites-1",
            query_params={"some_param": "12"},
        )
