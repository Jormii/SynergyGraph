from __future__ import annotations

import math
from typing import List, Set

from action import Action
from subject import Subject
from synergy_graph import IPredicate, SynonymFilter, Synergy, SynergyGraph


class Chain(IPredicate):

    def __init__(self, predicates: List[IPredicate]) -> None:
        super().__init__()

        self.predicates = predicates

    def roots(self) -> Set[Subject]:
        roots: Set[Subject] = set()
        for predicate in self.predicates:
            roots.update(predicate.roots())

        return roots

    def actions(self) -> Set[Action]:
        actions: Set[Action] = set()
        for predicate in self.predicates:
            actions.update(predicate.actions())

        return actions

    def tails(self) -> Set[Subject]:
        tails: Set[Subject] = set()
        for predicate in self.predicates:
            tails.update(predicate.tails())

        return tails

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        tmp: List[Synergy.Instance] = []
        new_instances: List[Synergy.Instance] = [instance]
        for predicate in self.predicates:
            tmp = list(new_instances)
            new_instances.clear()

            for new_instance in tmp:
                new_instances.extend(
                    predicate.traverse(graph, new_instance, out_synergy))

        return new_instances

    def _stringify(self, indentation: int = 0) -> str:
        s = (indentation * "\t") + f"<<CHAIN> [\n"
        for predicate in self.predicates:
            s += f"{predicate.stringify(indentation + 1)}\n"
        s += (indentation * "\t") + "]>"

        return s


class Execute(IPredicate):

    def __init__(self, subject: Subject, executes: Action, on: Subject) -> None:
        super().__init__()

        self.subject = subject
        self.executes = executes
        self.on = on

    def roots(self) -> Set[Subject]:
        return {self.subject}

    def actions(self) -> Set[Action]:
        return {self.executes}

    def tails(self) -> Set[Subject]:
        return {self.on}

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        new_instances: List[Synergy.Instance] = []
        synonyms = graph.get_synonyms(self.on, SynonymFilter.IS)
        for synonym in synonyms:
            predicate = self.derivative(
                Execute(self.subject, self.executes, synonym))
            new_instances.append(instance.copy_and_append(predicate))

        return new_instances

    def _stringify(self, indentation: int) -> str:
        return (indentation * "\t") + f"<EXE> {self.executes}({self.subject}, {self.on})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Execute):
            return False

        return self.subject == __o.subject and \
            self.executes == __o.executes and \
            self.on == __o.on

    def __hash__(self) -> int:
        return hash((self.subject, self.executes, self.on))


class Witness(IPredicate):

    def __init__(self, subject: Subject, witnesses: Action, on: Subject) -> None:
        super().__init__()

        self.subject = subject
        self.witnesses = witnesses
        self.on = on

    def roots(self) -> Set[Subject]:
        return {self.subject}

    def actions(self) -> Set[Action]:
        return {self.witnesses}

    def tails(self) -> Set[Subject]:
        return set()

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        new_instances: List[Synergy.Instance] = []
        inputs = graph.get_action_inputs(self.witnesses)
        for input in inputs:
            if not instance.predicate_visited(input) and self.on in input.tails():
                new_instances.append(
                    instance.copy_and_append(input, increment_score=False))

        return new_instances

    def _stringify(self, indentation: int) -> str:
        return (indentation * "\t") + f"<SEE> {self.witnesses}({self.subject}, {self.on})"

    def equal(self, predicate: Witness) -> bool:
        return self.subject == predicate.subject and \
            self.witnesses == predicate.witnesses and \
            self.on == predicate.on

    def __hash__(self) -> int:
        return hash((self.subject, self.witnesses, self.on))


class Multiplier(IPredicate):

    def __init__(self, predicate: IPredicate, factor: float = 1) -> None:
        super().__init__()

        self.predicate = predicate
        self.factor = factor

    def roots(self) -> Set[Subject]:
        return self.predicate.roots()

    def actions(self) -> Set[Action]:
        return self.predicate.actions()

    def tails(self) -> Set[Subject]:
        return self.predicate.tails()

    def equal(self, predicate: Multiplier) -> bool:
        return self.predicate == predicate.predicate and \
            math.isclose(self.factor, predicate.factor)

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        new_instances = self.predicate.traverse(graph, instance, out_synergy)
        for new_instance in new_instances:
            new_instance.score *= self.factor

        return new_instances

    def _stringify(self, indentation: int) -> str:
        s = (indentation * "\t") + \
            f"{self.factor:.2f} * {self.predicate.stringify(0)}"

        s = (indentation * "\t") + "<<MULT>\n"
        s += ((indentation + 1) * "\t") + f"{self.factor:.2f}x\n"
        s += f"{self.predicate.stringify(indentation + 1)}\n"
        s += (indentation * "\t") + ">"

        return s

    def __hash__(self) -> int:
        return hash((self.predicate, self.factor))


class Conditional(IPredicate):

    def __init__(self, condition: IPredicate, result: IPredicate) -> None:
        super().__init__()

        self.condition = condition
        self.result = result

    def roots(self) -> Set[Subject]:
        return self.condition.roots()

    def actions(self) -> Set[Action]:
        c_actions = self.condition.actions()
        r_actions = self.result.actions()

        return c_actions.union(r_actions)

    def tails(self) -> Set[Subject]:
        return self.result.tails()

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        condition_synergy = Synergy()
        self.condition.traverse(
            graph, instance.copy_and_append(self, increment_score=False), condition_synergy)

        assert len(condition_synergy.by_predicate) <= 1

        new_instances: List[Synergy.Instance] = []
        for condition_instances in condition_synergy.by_predicate.values():
            for condition_instance in condition_instances:
                new_instances.extend(
                    self.result.traverse(graph, condition_instance, out_synergy))

        return new_instances

    def _stringify(self, indentation: int) -> str:
        s = (indentation * "\t") + "<<IF>\n"
        s += f"{self.condition.stringify(indentation + 1)}\n"
        s += (indentation * "\t") + "<THEN>\n"
        s += f"{self.result.stringify(indentation + 1)}\n"
        s += (indentation * "\t") + ">"

        return s

    def equal(self, predicate: Conditional) -> bool:
        return self.condition == predicate.condition and \
            self.result == predicate.result

    def __hash__(self) -> int:
        return hash((self.condition, self.result))
