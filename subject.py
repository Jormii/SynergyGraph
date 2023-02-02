from enum import IntEnum


class SubjectTag(IntEnum):
    BASIC = 0
    CHARACTER = 1
    ANY = 2


class Subject:

    def __init__(self, name: str, tag:  SubjectTag) -> None:
        self.name = name
        self.tag = tag

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Subject):
            return False

        return self.name == __o.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{self.name}"
