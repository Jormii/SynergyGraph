from __future__ import annotations

from typing import Dict, List, Set

from action import Action
from subject import Subject
from predicate import IPredicate


class SynergyGraph:

    class Node:

        def __init__(self) -> None:
            self.inputs: Set[Action] = set()
            self.outputs: Set[IPredicate] = set()

        def add_input(self, predicate: IPredicate) -> None:
            self.inputs.add(predicate)

        def add_output(self, predicate: IPredicate) -> None:
            self.outputs.add(predicate)

        def __repr__(self) -> str:
            s = ""

            s += "- IN:\n"
            for input in self.inputs:
                s += f"{input}\n"

            s += "- OUT:\n"
            for output in self.outputs:
                s += f"{output}\n"

            return s

    def __init__(self) -> None:
        self.subjects: Dict[Subject, SynergyGraph.Node] = {}

    def subject_present(self, subject: Subject) -> bool:
        return subject in self.subjects

    def get_subject_node(self, subject: Subject) -> SynergyGraph.Node:
        return self.subjects[subject]

    def add_predicate(self, predicate: IPredicate) -> None:
        for subpredicate in predicate.unwrap():
            head = subpredicate.head()
            tail = subpredicate.tail()
            action = subpredicate.action()

            self._get_or_create_subject_node(tail).add_input(action)
            self._get_or_create_subject_node(head).add_output(predicate)

    def _get_or_create_subject_node(self, subject: Subject) -> SynergyGraph.Node:
        if not self.subject_present(subject):
            self.subjects[subject] = SynergyGraph.Node()

        return self.get_subject_node(subject)

    def __repr__(self) -> str:
        s = ""
        for subject, node in self.subjects.items():
            s += f"-- {subject.name} --\n{node}\n"

        return s
