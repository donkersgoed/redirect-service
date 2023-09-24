# Standard library imports
from dataclasses import dataclass
from enum import Enum

# Local application / library specific imports
from . import BaseDataclass


@dataclass
class Alias(BaseDataclass):
    pk: str
    sk: str
    alias_domain: str

    @classmethod
    def from_ddb_item(cls, item: dict) -> "Alias":
        return cls(
            pk=item["pk"],
            sk=item["sk"],
            alias_domain=item["alias"],
        )


class RedirectType(str, Enum):
    EXACT = "EXACT"
    BEGINS_WITH = "BEGINS_WITH"


@dataclass
class RedirectOption(BaseDataclass):
    domain: str
    path: str
    target: str
    type: RedirectType

    @classmethod
    def from_ddb_item(cls, item: dict) -> "RedirectOption":
        pk: str = item["pk"]
        return cls(
            domain=pk.lstrip("Redirect#"),
            path=item["sk"],
            target=item["target"],
            type=RedirectType(item["type"]),
        )
