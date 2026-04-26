from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class UserDTO:
    username: str
    uid: str
    email: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)
