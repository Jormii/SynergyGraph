from typing import Set

from action import Action
from subject import Subject
from synergy_graph import IPredicate, Synergy, SynergyGraph


class Execute(IPredicate):

    def __init__(self, subject: Subject, executes: Action, on: Subject) -> None:
        self.subject = subject
        self.executes = executes
        self.on = on

    def roots(self) -> Set[Subject]:
        return {self.subject}

    def actions(self) -> Set[Action]:
        return {self.executes}

    def tails(self) -> Set[Subject]:
        return {self.on}

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        out_synergy.add(instance)

    def __repr__(self) -> str:
        return f"<EXE> {self.executes}({self.subject}, {self.on})"


class Witness(IPredicate):

    def __init__(self, subject: Subject, witnesses: Action, on: Subject) -> None:
        self.subject = subject
        self.witnesses = witnesses
        self.on = on

    def roots(self) -> Set[Subject]:
        return {self.subject}

    def actions(self) -> Set[Action]:
        return {self.witnesses}

    def tails(self) -> Set[Subject]:
        return {self.on}

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        inputs = graph.get_action_inputs(self.witnesses)
        for input in inputs:
            if not instance.predicate_present(input) and self.on in input.tails():
                out_synergy.add(instance.copy_and_append(input))

    def __repr__(self) -> str:
        return f"<SEE> {self.witnesses}({self.subject}, {self.on})"


class Conditional(IPredicate):

    def __init__(self, condition: IPredicate, result: IPredicate) -> None:
        self.condition = condition
        self.result = result

    def __repr__(self) -> str:
        return f"<<IF> ({self.condition})> <THEN> ({self.result})>>"
