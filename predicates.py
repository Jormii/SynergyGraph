from typing import List

from action import Action
from subject import Subject
from predicate import IPredicate


class Execution(IPredicate):

    def __init__(self, subject: Subject, executes: Action, on: Subject) -> None:
        self.subject = subject
        self.executes = executes
        self.on = on

    def head(self) -> Subject:
        return self.subject

    def action(self) -> Action:
        return self.executes

    def tail(self) -> Subject:
        return self.on

    def unwrap(self) -> List[IPredicate]:
        return [self]

    def __repr__(self) -> str:
        return f"{self.executes}({self.subject}, {self.on})"


class Conditional(IPredicate):

    def __init__(self, condition: IPredicate, result: IPredicate) -> None:
        self.condition = condition
        self.result = result

    def head(self) -> Subject:
        return self.condition.head()

    def unwrap(self) -> List[IPredicate]:
        unwrapped = []
        for predicate in [self.condition, self.result]:
            unwrapped.extend(predicate.unwrap())

        return unwrapped

    def __repr__(self) -> str:
        return f"<<IF>> {self.condition} <<THEN>> {self.result}"
