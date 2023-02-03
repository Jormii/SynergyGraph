from __future__ import annotations

from typing import Dict, Set

from action import Action
from subject import Subject
from predicate import IPredicate


class SynergyGraph:

    def __init__(self) -> None:
        self.actions: Dict[Action, Set[IPredicate]] = {}
        self.subjects: Dict[Subject, Set[IPredicate]] = {}

    def add_predicate(self, predicate: IPredicate) -> None:
        head = predicate.head()
        self.get_subject_outputs(head).add(predicate)

        for subpredicate in predicate.unwrap():
            action = subpredicate.action()
            self.get_action_inputs(action).add(predicate)

    def get_action_inputs(self, action: Action) -> Set[IPredicate]:
        if action not in self.actions:
            self.actions[action] = set()

        return self.actions[action]

    def get_subject_outputs(self, subject: Subject) -> Set[IPredicate]:
        if subject not in self.subjects:
            self.subjects[subject] = set()

        return self.subjects[subject]

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
