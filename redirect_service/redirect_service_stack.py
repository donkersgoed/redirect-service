"""The module containing all the resources of the redirect service."""

# Related third party imports
from aws_cdk import Stack
from constructs import Construct

# Local application / library specific imports
from redirect_service.constructs.proxy import Proxy
from redirect_service.constructs.process import Process
from redirect_service.constructs.storage import Storage


class RedirectServiceStack(Stack):
    """The class containing all the resources of the redirect service."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Construct a new RedirectServiceStack class."""
        super().__init__(scope, construct_id, **kwargs)

        storage = Storage(scope=self, construct_id="Storage")
        proxy = Proxy(scope=self, construct_id="Proxy")
        Process(
            scope=self,
            construct_id="Process",
            proxy_api=proxy.rest_api,
            ddb_table=storage.ddb_table,
        )
