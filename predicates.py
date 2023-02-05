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
        if instance.predicate_visited(self):
            return

        out_synergy.add(instance.copy_and_append(1, self))

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
        return set()

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        inputs = graph.get_action_inputs(self.witnesses)
        for input in inputs:
            if not instance.predicate_visited(input) and self.on in input.tails():
                out_synergy.add(instance.copy_and_append(0, input))

    def __repr__(self) -> str:
        return f"<SEE> {self.witnesses}({self.subject}, {self.on})"


class Conditional(IPredicate):

    def __init__(self, condition: IPredicate, result: IPredicate, chance: float = 1) -> None:
        self.condition = condition
        self.result = result
        self.chance = chance

    def roots(self) -> Set[Subject]:
        return self.condition.roots()

    def actions(self) -> Set[Action]:
        c_actions = self.condition.actions()
        r_actions = self.result.actions()

        return c_actions.union(r_actions)

    def tails(self) -> Set[Subject]:
        return self.result.tails()

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        condition_synergy = Synergy()
        self.condition.traverse(
            graph, instance.copy_and_append(0, self), condition_synergy)

        assert len(condition_synergy.by_predicate) <= 1

        for condition_instances in condition_synergy.by_predicate.values():
            for condition_instance in condition_instances:
                condition_score = condition_instance.score - instance.score
                condition_instance.score -= condition_score
                condition_instance.score += self.chance * condition_score

                self.result.traverse(graph, condition_instance, out_synergy)

    def __repr__(self) -> str:
        return f"<<IF> ({self.condition})> <THEN> ({self.result})>>"
