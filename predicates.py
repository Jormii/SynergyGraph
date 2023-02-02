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

    def tails(self) -> List[Subject]:
        return [self.on]

    def unwrap(self) -> List[IPredicate]:
        return [self]


class Conditional(IPredicate):

    def __init__(self, condition: IPredicate, result: IPredicate) -> None:
        self.condition = condition
        self.result = result

    def unwrap(self) -> List[IPredicate]:
        unwrapped = []
        for predicate in [self.condition, self.result]:
            unwrapped.extend(predicate.unwrap())

        return unwrapped
