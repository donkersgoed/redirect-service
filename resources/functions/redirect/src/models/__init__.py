"""Module for shared classes across all models."""

import dataclasses


@dataclasses.dataclass
class BaseDataclass:
    """The BaseDataclass, used to conveniently supply common dataclass methods."""

    def as_dict(self) -> dict:
        """Return the dataclass in dict representation."""
        return dataclasses.asdict(self)
