from __future__ import annotations
from enum import IntEnum
from typing import Dict, List, Set, Union

from action import Action
from subject import Subject

INDENT_SIZE = 4


class SynonymFilter(IntEnum):
    IS = 0
    OTHERS_ARE = 1


class IPredicate:

    def __init__(self, annotation: str) -> None:
        self.annotation = annotation
        self.derived_from: IPredicate = None

    def derivative(self, predicate: IPredicate) -> IPredicate:
        assert type(self) == type(predicate) and self != predicate

        predicate.derived_from = self
        return predicate

    def traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        new_instances: List[Synergy.Instance] = []
        if not instance.predicate_visited(self):
            new_instances = self._traverse(graph, instance, out_synergy)

        for new_instance in new_instances:
            out_synergy.add(new_instance)

        return new_instances

    def stringify(self, indentation: int):
        s = ""
        if len(self.annotation) != 0:
            s += f"{self._indent(indentation)}\"{self.annotation}\"\n"

        s += self._stringify(indentation)
        if self.derived_from is not None:
            s += f"(<DF> {self.derived_from.stringify(indentation)})"

        return s

    def _get(self) -> IPredicate:
        if self.derived_from is None:
            return self
        else:
            return self.derived_from

    def _indent(self, indentation: int) -> str:
        return indentation * (INDENT_SIZE * " ")

    def actors(self) -> Set[Subject]:
        raise NotImplementedError(type(self))

    def objectives(self) -> Set[Subject]:
        raise NotImplementedError(type(self))

    def actions(self) -> Set[Action]:
        raise NotImplementedError(type(self))

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        raise NotImplementedError(type(self))

    def _equals(self, predicate: IPredicate) -> bool:
        raise NotImplementedError(type(self))

    def _hash(self) -> int:
        raise NotImplementedError(type(self))

    def _stringify(self, indentation: int) -> str:
        raise NotImplementedError(type(self))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self._get()._equals(__o._get())
        else:
            return False

    def __hash__(self) -> int:
        return self._get()._hash()

    def __repr__(self) -> str:
        return self.stringify(0)


class Synergy:

    class Instance:

        def __init__(self, score: int, predicates: Union[IPredicate, List[IPredicate]]) -> None:
            if not isinstance(predicates, list):
                predicates = [predicates]

            self.score = score
            self.predicates: List[IPredicate] = predicates
            self.visited: Set[IPredicate] = set(self.predicates)

        def root_predicate(self) -> IPredicate:
            return self.predicates[0]

        def tail_predicate(self) -> IPredicate:
            return self.predicates[-1]

        def predicate_visited(self, predicate: IPredicate) -> bool:
            return predicate in self.visited

        def copy_and_append(self, predicate: IPredicate, increment_score: bool = True) -> Synergy.Instance:
            predicates = list(self.predicates)
            predicates.append(predicate)

            copy = Synergy.Instance(self.score + increment_score, predicates)
            return copy

        def __repr__(self) -> str:
            s = f"SCORE: {self.score:.2f}, [\n"
            for predicate in self.predicates:
                s += f"{INDENT_SIZE * ' '}{predicate}\n"

            s += "]"

            return s

        def root_instance() -> Synergy.Instance:
            return Synergy.Instance(0, [])

    def __init__(self) -> None:
        self.synergies: Dict[IPredicate, List[Synergy.Instance]] = {}

    def add(self, instance: Synergy.Instance) -> None:
        predicate = instance.root_predicate()

        if predicate not in self.synergies:
            self.synergies[predicate] = []
        self.synergies[predicate].append(instance)

    def extend(self, synergy: Synergy) -> None:
        for instances in synergy.synergies.values():
            for instance in instances:
                self.add(instance)

    def __repr__(self) -> str:
        s = "----- Synergies -----\n"
        for predicate, instances in self.synergies.items():
            s += f"- {predicate}\n"
            for instance in instances:
                s += f"-- {instance}\n"

        return s


class SynergyGraph:

    class SubjectNode:

        def __init__(self):
            self.synonyms_in: Set[Subject] = set()
            self.synonyms_out: Set[Subject] = set()
            self.predicates: Set[IPredicate] = set()

    def __init__(self) -> None:
        self.actions: Dict[Action, Set[IPredicate]] = {}
        self.subjects: Dict[Subject, SynergyGraph.SubjectNode] = {}

    def add_synonym(self, subject: Subject, is_a: Subject) -> None:
        if subject != is_a:
            self.get_subject_node(subject).synonyms_out.add(is_a)
            self.get_subject_node(is_a).synonyms_in.add(subject)

    def add_predicate(self, predicate: IPredicate) -> None:
        for actor in predicate.actors():
            self.get_subject_node(actor).predicates.add(predicate)

        for action in predicate.actions():
            self.get_action_inputs(action).add(predicate)

    def get_synonyms(self, subject: Subject, filter: SynonymFilter) -> Set[Subject]:
        node = self.get_subject_node(subject)
        if filter == SynonymFilter.IS:
            synonyms_src = node.synonyms_out
        elif filter == SynonymFilter.OTHERS_ARE:
            synonyms_src = node.synonyms_in

        synonyms: Set[Subject] = {subject}
        queue: List[Subject] = list(synonyms_src)
        while len(queue) != 0:
            aka = queue.pop(0)
            synonyms.add(aka)
            aka_synonyms = self.get_synonyms(aka, filter)

            aka_synonyms = aka_synonyms.difference(synonyms)
            queue.extend(aka_synonyms)

        return synonyms

    def get_action_inputs(self, action: Action) -> Set[IPredicate]:
        if action not in self.actions:
            self.actions[action] = set()

        return self.actions[action]

    def get_subject_node(self, subject: Subject) -> SynergyGraph.SubjectNode:
        if subject not in self.subjects:
            self.subjects[subject] = SynergyGraph.SubjectNode()

        return self.subjects[subject]

    def all_synergies(self) -> Synergy:
        synergy = Synergy()
        for subject in self.subjects.keys():
            synergy.extend(self.synergies(subject))

        return synergy

    def synergies(self, subject: Subject) -> Synergy:
        synergy = Synergy()
        for predicate in self.get_subject_node(subject).predicates:
            predicate_synergy = self.predicate_synergies(predicate)
            synergy.extend(predicate_synergy)

        return synergy

    def predicate_synergies(self, predicate: IPredicate) -> Synergy:
        synergy = Synergy()
        predicate.traverse(self, Synergy.Instance.root(), synergy)

        return synergy

    def __repr__(self) -> str:
        s = ""

        s += "[[[ Graph actions ]]]\n"
        for action, predicates in self.actions.items():
            s += f"- {action}\n"
            for predicate in predicates:
                s += f"-- {predicate}\n"

        s += "\n[[[ Graph subjects ]]]\n"
        for subject, node in self.subjects.items():
            s += f"- {subject}\n"
            s += f"- (X are {subject}): {node.synonyms_in}\n"
            s += f"- ({subject} is X): {node.synonyms_out}\n"
            for predicate in node.predicates:
                s += f"-- {predicate}\n"

            s += "\n"

        return s
