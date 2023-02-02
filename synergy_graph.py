from __future__ import annotations

from typing import Dict, Set

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

    def add_predicate(self, predicate: IPredicate) -> None:
        # Head
        head = predicate.head()
        self._get_subject_node(head).add_output(predicate)

        # Tails
        for subpredicate in predicate.unwrap():
            tail = subpredicate.tail()
            action = subpredicate.action()
            self._get_subject_node(tail).add_input(action)

    def _get_subject_node(self, subject: Subject) -> SynergyGraph.Node:
        if subject not in self.subjects:
            self.subjects[subject] = SynergyGraph.Node()

        return self.subjects[subject]

    def __repr__(self) -> str:
        s = ""
        for subject, node in self.subjects.items():
            s += f"-- {subject.name} --\n{node}\n"

        return s
