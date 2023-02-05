from __future__ import annotations

import math
from typing import Set

from action import Action
from subject import Subject
from synergy_graph import IPredicate, SynonymFilter, Synergy, SynergyGraph


# TODO: Somewhat messy
class Equivalent(IPredicate):

    def __init__(self, original: IPredicate, equivalent: IPredicate) -> None:
        self.original = original
        self.equivalent = equivalent

    def roots(self) -> Set[Subject]:
        return self.equivalent.roots()

    def tails(self) -> Set[Subject]:
        return self.equivalent.tails()

    def equal(self, predicate: Equivalent) -> bool:
        return self.original == predicate.original

    def __hash__(self) -> int:
        return hash(self.original)

    def __repr__(self) -> str:
        if self.original == self.equivalent:
            return repr(self.original)
        else:
            return f"<EQ> ({self.equivalent}) <=== ({self.original})"


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

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        synonyms = graph.get_synonyms(self.on, SynonymFilter.OUTPUT)
        for synonym in synonyms:
            predicate = Equivalent(
                self, Execute(self.subject, self.executes, synonym))
            out_synergy.add(instance.copy_and_append(1, predicate))

    def equal(self, predicate: Execute) -> bool:
        return self.subject == predicate.subject and \
            self.executes == predicate.executes and \
            self.on == predicate.on

    def __hash__(self) -> int:
        return hash((self.subject, self.executes, self.on))

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

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        inputs = graph.get_action_inputs(self.witnesses)
        for input in inputs:
            if not instance.predicate_visited(input) and self.on in input.tails():
                out_synergy.add(instance.copy_and_append(0, input))

    def equal(self, predicate: Witness) -> bool:
        return self.subject == predicate.subject and \
            self.witnesses == predicate.witnesses and \
            self.on == predicate.on

    def __hash__(self) -> int:
        return hash((self.subject, self.witnesses, self.on))

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

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
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

    def equal(self, predicate: Conditional) -> bool:
        return self.condition == predicate.condition and \
            self.result == predicate.result and \
            math.isclose(self.chance, predicate.chance)

    def __hash__(self) -> int:
        return hash((self.condition, self.result, self.chance))

    def __repr__(self) -> str:
        return f"<<IF> ({self.condition})> <THEN> ({self.result})>>"
