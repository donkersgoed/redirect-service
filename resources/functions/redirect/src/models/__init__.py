import dataclasses


@dataclasses.dataclass
class BaseDataclass:
    def as_dict(self) -> dict:
        return dataclasses.asdict(self)
