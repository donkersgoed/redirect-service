"""Module for database models, representing data found in DDB."""

# Standard library imports
from dataclasses import dataclass

# Local application / library specific imports
from . import BaseDataclass


@dataclass
class Alias(BaseDataclass):
    """The Alias model, representing an DomainAlias in the database."""

    source_domain: str
    target_domain: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "Alias":
        """Convert a DDB item to an Alias object."""
        partition_key: str = item["pk"]
        return cls(
            source_domain=partition_key.lstrip("DomainAlias#"),
            target_domain=item["target_domain"],
        )


@dataclass
class RedirectOption(BaseDataclass):
    """The RedirectOption model, representing an RedirectOption in the database."""

    domain: str
    path: str
    target: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "RedirectOption":
        """Convert a DDB item to an RedirectOption object."""
        partition_key: str = item["pk"]
        return cls(
            domain=partition_key.lstrip("Redirect#"),
            path=item["sk"],
            target=item["target"],
        )


@dataclass
class RedirectFallbackOption(BaseDataclass):
    """The RedirectFallbackOption model, representing an RedirectFallbackOption in the database."""

    domain: str
    path: str
    target: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "RedirectFallbackOption":
        """Convert a DDB item to an RedirectFallbackOption object."""
        partition_key: str = item["pk"]
        return cls(
            domain=partition_key.lstrip("RedirectFallback#"),
            path=item["sk"],
            target=item["target"],
        )
