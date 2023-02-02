class Action:

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Action):
            return False

        return self.name == __o.name

    def __hash__(self) -> int:
        return hash(self.name)
