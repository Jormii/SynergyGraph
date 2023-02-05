from __future__ import annotations

from typing import Dict, List, Set

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

        def __init__(self, predicate: IPredicate) -> None:
            self.visited: Set[IPredicate] = {predicate}
            self.predicates: List[IPredicate] = [predicate]

        def root_predicate(self) -> IPredicate:
            return self.predicates[0]

        def tail_predicate(self) -> IPredicate:
            return self.predicates[-1]

        def predicate_present(self, predicate: IPredicate) -> bool:
            return predicate in self.visited

        def copy_and_replace_with(self, predicate: IPredicate) -> Synergy.Instance:
            copy = Synergy.Instance(predicate)
            copy.visited.update(self.visited)

            return copy

        def copy_and_append(self, predicate: IPredicate) -> Synergy.Instance:
            copy = Synergy.Instance(self.root_predicate())

            copy.visited.add(predicate)

            copy.predicates.extend(self.predicates[1:])
            copy.predicates.append(predicate)

            return copy

        def __repr__(self) -> str:
            return f"{self.predicates}"

    def __init__(self) -> None:
        self.by_subject: Dict[Subject, List[Synergy.Instance]] = {}
        self.by_predicate: Dict[IPredicate, List[Synergy.Instance]] = {}

    def add(self, instance: Synergy.Instance) -> None:
        predicate = instance.root_predicate()

        for root in predicate.roots():
            if root not in self.by_subject:
                self.by_subject[root] = []

            self.by_subject[root].append(instance)

        if predicate not in self.by_predicate:
            self.by_predicate[predicate] = []
        self.by_predicate[predicate].append(instance)

    def extend(self, synergy: Synergy) -> None:
        self.by_subject.update(synergy.by_subject)
        self.by_predicate.update(synergy.by_predicate)

    def __repr__(self) -> str:
        s = "Synergies by subject\n"
        for subject, synergies in self.by_subject.items():
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
        root_instance = Synergy.Instance(predicate)
        predicate.traverse(self, root_instance, synergy)

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
