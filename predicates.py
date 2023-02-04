from typing import List

from action import Action
from subject import Subject
from synergy_graph import IPredicate, Synergy, SynergyGraph


class Execute(IPredicate):

    def __init__(self, subject: Subject, executes: Action, on: Subject) -> None:
        self.subject = subject
        self.executes = executes
        self.on = on

    def head(self) -> Subject:
        return self.subject

    def action(self) -> Action:
        return self.executes

    def unwrap(self) -> List[IPredicate]:
        return [self]

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        out_synergy.add(instance)

    def __repr__(self) -> str:
        return f"<EXE> {self.executes}({self.subject}, {self.on})"


class Witness(IPredicate):

    def __init__(self, subject: Subject, witnesses: Action, on: Subject) -> None:
        self.subject = subject
        self.witnesses = witnesses
        self.on = on

    def head(self) -> Subject:
        return self.subject

    def action(self) -> Action:
        return self.witnesses

    def unwrap(self) -> List[IPredicate]:
        return [self]

    def __repr__(self) -> str:
        return f"<SEE> {self.witnesses}({self.subject}, {self.on})"


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
        return f"<<IF> ({self.condition})> <THEN> ({self.result})>>"
