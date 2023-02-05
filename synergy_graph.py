from __future__ import annotations

from typing import Dict, List, Set, Union

from action import Action
from subject import Subject


class IPredicate:

    def roots(self) -> Set[Subject]:
        raise NotImplementedError(type(self))

    def actions(self) -> Set[Action]:
        raise NotImplementedError(type(self))

    def tails(self) -> Set[Subject]:
        raise NotImplementedError(type(self))

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        raise NotImplementedError(type(self))


class Synergy:

    class Instance:

        def __init__(self, score: int, predicates: Union[IPredicate, List[IPredicate]]) -> None:
            if not isinstance(predicates, list):
                predicates = [predicates]

            self.score = score
            self.predicates: List[IPredicate] = predicates
            self.visited: Set[IPredicate] = set(self.predicates)

        @staticmethod
        def root() -> Synergy.Instance:
            return Synergy.Instance(0, [])

        def root_predicate(self) -> IPredicate:
            return self.predicates[0]

        def tail_predicate(self) -> IPredicate:
            return self.predicates[-1]

        def predicate_visited(self, predicate: IPredicate) -> bool:
            return predicate in self.visited

        def copy_and_append(self, score: int, predicate: IPredicate) -> Synergy.Instance:
            predicates = list(self.predicates)
            predicates.append(predicate)

            copy = Synergy.Instance(self.score + score, predicates)
            return copy

        def __repr__(self) -> str:
            return f"SCORE: {self.score:.2f}, {self.predicates}"

    def __init__(self) -> None:
        self.by_performer: Dict[Subject, List[Synergy.Instance]] = {}
        self.by_beneficiary: Dict[Subject, List[Synergy.Instance]] = {}
        self.by_predicate: Dict[IPredicate, List[Synergy.Instance]] = {}

    def add(self, instance: Synergy.Instance) -> None:
        predicate = instance.root_predicate()

        for root in predicate.roots():
            if root not in self.by_performer:
                self.by_performer[root] = []

            self.by_performer[root].append(instance)

        for tail in predicate.tails():
            if tail not in self.by_beneficiary:
                self.by_beneficiary[tail] = []

            self.by_beneficiary[tail].append(instance)

        if predicate not in self.by_predicate:
            self.by_predicate[predicate] = []
        self.by_predicate[predicate].append(instance)

    def extend(self, synergy: Synergy) -> None:
        for subject, predicates in synergy.by_performer.items():
            if subject not in self.by_performer:
                self.by_performer[subject] = list(predicates)
            else:
                self.by_performer[subject].extend(predicates)

        for subject, predicates in synergy.by_beneficiary.items():
            if subject not in self.by_beneficiary:
                self.by_beneficiary[subject] = list(predicates)
            else:
                self.by_beneficiary[subject].extend(predicates)

        for predicate, predicates in synergy.by_predicate.items():
            if predicate not in self.by_predicate:
                self.by_predicate[predicate] = list(predicates)
            else:
                self.by_predicate[predicate].extend(predicates)

    def __repr__(self) -> str:
        s = "Synergies by performer\n"
        for subject, synergies in self.by_performer.items():
            s += f"- {subject}\n"
            for synergy in synergies:
                s += f"-- {synergy}\n"

        s += "\nSynergies by beneficiary\n"
        for subject, synergies in self.by_beneficiary.items():
            s += f"- {subject}\n"
            for synergy in synergies:
                s += f"-- {synergy}\n"

        s += "\nSynergies by predicate\n"
        for predicate, synergies in self.by_predicate.items():
            s += f"- {predicate}\n"
            for synergy in synergies:
                s += f"-- {synergy}\n"

        return s


class SynergyGraph:

    def __init__(self) -> None:
        self.actions: Dict[Action, Set[IPredicate]] = {}
        self.subjects: Dict[Subject, Set[IPredicate]] = {}

    def add_predicate(self, predicate: IPredicate) -> None:
        for root in predicate.roots():
            self.get_subject_outputs(root).add(predicate)

        for action in predicate.actions():
            self.get_action_inputs(action).add(predicate)

    def get_action_inputs(self, action: Action) -> Set[IPredicate]:
        if action not in self.actions:
            self.actions[action] = set()

        return self.actions[action]

    def get_subject_outputs(self, subject: Subject) -> Set[IPredicate]:
        if subject not in self.subjects:
            self.subjects[subject] = set()

        return self.subjects[subject]

    def synergies(self, subject: Subject) -> Synergy:
        synergy = Synergy()
        for predicate in self.get_subject_outputs(subject):
            predicate_synergy = self.predicate_synergies(predicate)
            synergy.extend(predicate_synergy)

        return synergy

    def predicate_synergies(self, predicate: IPredicate) -> Synergy:
        synergy = Synergy()
        predicate.traverse(self, Synergy.Instance.root(), synergy)

        return synergy

    def __repr__(self) -> str:
        s = ""

        s += "Graph actions\n"
        for action, predicates in self.actions.items():
            s += f"- {action}\n"
            for predicate in predicates:
                s += f"-- {predicate}\n"

        s += "\nGraph subjects\n"
        for subject, predicates in self.subjects.items():
            s += f"- {subject}\n"
            for predicate in predicates:
                s += f"-- {predicate}\n"

        return s
