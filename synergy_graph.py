from __future__ import annotations
from enum import IntEnum, auto
from typing import Dict, List, Set, Union

from action import Action
from subject import Subject

INDENT_SIZE = 4


class SynonymFilter(IntEnum):
    IS = auto()
    OTHERS_ARE = auto()


class IPredicate:

    def __init__(self, annotation: str) -> None:
        self.annotation = annotation
        self._derived_from: IPredicate = None

    def derive(self, predicate: IPredicate) -> IPredicate:
        if self == predicate:
            return self

        assert type(self) == type(predicate)

        predicate._derived_from = self
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
        if self._derived_from is not None:
            s += f"(<DF> {self._derived_from.stringify(indentation)})"

        return s

    def original(self) -> IPredicate:
        if self._derived_from is None:
            return self
        else:
            return self._derived_from

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
            return self.original()._equals(__o.original())
        else:
            return False

    def __hash__(self) -> int:
        return self.original()._hash()

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

        def root_instance() -> Synergy.Instance:
            return Synergy.Instance(0, [])

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

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Synergy.Instance):
                return False

            return self.predicates == __o.predicates

        def __hash__(self) -> int:
            return hash(tuple(self.predicates))

        def __repr__(self) -> str:
            s = f"SCORE: {self.score:.2f}, [\n"
            for predicate in self.predicates:
                s += f""
                if len(predicate.annotation) == 0:
                    s += f"{predicate.stringify(1)}\n"
                else:
                    s += f"{INDENT_SIZE * ' '}{predicate.annotation}\n"

            s += "]"

            return s

    def __init__(self) -> None:
        self.synergies: Dict[IPredicate, Set[Synergy.Instance]] = {}

    def add(self, instance: Synergy.Instance) -> None:
        predicate = instance.root_predicate()

        if predicate not in self.synergies:
            self.synergies[predicate] = set()
        self.synergies[predicate].add(instance)

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
        for subject in list(self.subjects.keys()):
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
        predicate.traverse(self, Synergy.Instance.root_instance(), synergy)

        return synergy

    def print_subjects(self) -> None:
        print("[[[ Subjects ]]]")

        for subject in list(self.subjects.keys()):
            self.print_subject(subject)

    def print_subject(self, subject: Subject) -> None:
        node = self.get_subject_node(subject)

        print(f"- {subject}")
        print(f"- (X are {subject}): {node.synonyms_in}")
        print(f"- ({subject} is X): {node.synonyms_out}")
        for predicate in node.predicates:
            print(f"-- {predicate}")

    def print_actions(self) -> None:
        print("[[[ Actions ]]]")

        for action, predicates in self.actions.items():
            print(f"- {action}")
            for predicate in predicates:
                print(f"-- {predicate}")
