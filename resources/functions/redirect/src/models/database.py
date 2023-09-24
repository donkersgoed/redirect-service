# Standard library imports
from dataclasses import dataclass
from enum import Enum

# Local application / library specific imports
from . import BaseDataclass


@dataclass
class Alias(BaseDataclass):
    source_domain: str
    target_domain: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "Alias":
        pk: str = item["pk"]
        return cls(
            source_domain=pk.lstrip("DomainAlias#"),
            target_domain=item["target_domain"],
        )


@dataclass
class RedirectOption(BaseDataclass):
    domain: str
    path: str
    target: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "RedirectOption":
        pk: str = item["pk"]
        return cls(
            domain=pk.lstrip("Redirect#"),
            path=item["sk"],
            target=item["target"],
        )


@dataclass
class RedirectFallbackOption(BaseDataclass):
    domain: str
    path: str
    target: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "RedirectOption":
        pk: str = item["pk"]
        return cls(
            domain=pk.lstrip("RedirectFallback#"),
            path=item["sk"],
            target=item["target"],
        )
