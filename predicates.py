from __future__ import annotations
import math
from typing import List, Set

from action import Action
from subject import Subject
from synergy_graph import IPredicate, SynonymFilter, Synergy, SynergyGraph


class Execute(IPredicate):

    def __init__(self, actor: Subject, action: Action, objective: Subject, annotation: str = "") -> None:
        super().__init__(annotation)

        self.actor = actor
        self.action = action
        self.objective = objective

    def actors(self) -> Set[Subject]:
        return {self.actor}

    def objectives(self) -> Set[Subject]:
        return {self.objective}

    def actions(self) -> Set[Action]:
        return {self.action}

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        new_instances: List[Synergy.Instance] = []
        synonyms = graph.get_synonyms(self.objective, SynonymFilter.IS)
        for synonym in synonyms:
            predicate = self.derive(
                Execute(self.actor, self.action, synonym))
            new_instances.append(instance.copy_and_append(predicate))

        return new_instances

    def _equals(self, execute: Execute) -> bool:
        return self.actor == execute.actor \
            and self.action == execute.action \
            and self.objective == execute.objective

    def _hash(self) -> int:
        return hash((self.actor, self.action, self.objective))

    def _stringify(self, indentation: int) -> str:
        return f"{self._indent(indentation)}<EXE> {self.action}({self.actor}, {self.objective})"


class Conditional(IPredicate):

    def __init__(self, event: IPredicate, outcome: IPredicate, annotation: str = "") -> None:
        super().__init__(annotation)

        self.event = event
        self.outcome = outcome

    def actors(self) -> Set[Subject]:
        return self.event.actors()

    def objectives(self) -> Set[Subject]:
        return self.outcome.objectives()

    def actions(self) -> Set[Action]:
        return self.event.actions().union(self.outcome.actions())

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        return []   # TODO
        
        event_synergy = Synergy()
        self.event.traverse(
            graph, instance.copy_and_append(self, increment_score=False), event_synergy)

        assert len(event_synergy.synergies) <= 1

        new_instances: List[Synergy.Instance] = []
        for event_instances in event_synergy.synergies.values():
            for event_instance in event_instances:
                new_instances.extend(
                    self.outcome.traverse(graph, event_instance, out_synergy))

        return new_instances

    def _equals(self, predicate: Conditional) -> bool:
        return self.event == predicate.event \
            and self.outcome == predicate.outcome

    def _hash(self) -> int:
        return hash((self.event, self.outcome))

    def _stringify(self, indentation: int) -> str:
        s = f"{self._indent(indentation)}<<IF>\n"
        s += f"{self.event.stringify(indentation + 1)}\n"
        s += f"{self._indent(indentation)}<THEN>\n"
        s += f"{self.outcome.stringify(indentation + 1)}\n"
        s += f"{self._indent(indentation)}>"

        return s


class Multiplier(IPredicate):

    def __init__(self, predicate: IPredicate, factor: float, annotation: str = "") -> None:
        super().__init__(annotation)

        self.predicate = predicate
        self.factor = factor

    def actors(self) -> Set[Subject]:
        return self.predicate.actors()

    def objectives(self) -> Set[Subject]:
        return self.predicate.objectives()

    def actions(self) -> Set[Action]:
        return self.predicate.actions()

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> None:
        new_instances = self.predicate.traverse(graph, instance, out_synergy)
        for new_instance in new_instances:
            new_instance.score *= self.factor

        return new_instances

    def _equals(self, predicate: Multiplier) -> bool:
        return self.predicate == predicate.predicate \
            and math.isclose(self.factor, predicate.factor)

    def _hash(self) -> int:
        return hash((self.predicate, self.factor))

    def _stringify(self, indentation: int) -> str:
        s = f"{self._indent(indentation)}<<MULT>\n"
        s += f"{self._indent(indentation + 1)}{self.factor:.2f}x\n"
        s += f"{self.predicate.stringify(indentation + 1)}\n"
        s += f"{self._indent(indentation)}>"

        return s


class Repeat(IPredicate):

    def __init__(self, predicate: IPredicate, times: int, annotation: str = "") -> None:
        super().__init__(annotation)

        self.predicate = predicate
        self.times = times

    def actors(self) -> Set[Subject]:
        return self.predicate.actors()

    def objectives(self) -> Set[Subject]:
        return self.predicate.objectives()

    def actions(self) -> Set[Action]:
        return self.predicate.actions()

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        new_instances = self.predicate.traverse(
            graph, instance.copy_and_append(self, increment_score=False), out_synergy)

        for new_instance in new_instances:
            new_instance.score *= self.times

        return new_instances

    def _equals(self, predicate: Repeat) -> bool:
        return self.predicate == predicate.predicate \
            and self.times == predicate.times

    def _hash(self) -> int:
        return hash((self.predicate, self.times))

    def _stringify(self, indentation: int) -> str:
        s = f"{self._indent(indentation)}<<REPEAT>\n"
        s += f"{self._indent(indentation + 1)}{self.times} TIMES \n"
        s += f"{self.predicate.stringify(indentation + 1)}\n"
        s += f"{self._indent(indentation)}>"

        return s


class Chain(IPredicate):

    def __init__(self, predicates: List[IPredicate], annotation: str = "") -> None:
        super().__init__(annotation)

        self.predicates = predicates

    def actors(self) -> Set[Subject]:
        actors: Set[Subject] = set()
        for predicate in self.predicates:
            actors.update(predicate.actors())

        return actors

    def objectives(self) -> Set[Subject]:
        objectives: Set[Subject] = set()
        for predicate in self.predicates:
            objectives.update(predicate.objectives())

        return objectives

    def actions(self) -> Set[Action]:
        actions: Set[Action] = set()
        for predicate in self.predicates:
            actions.update(predicate.actions())

        return actions

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

    def _equals(self, predicate: Chain) -> bool:
        return self.predicates == predicate.predicates

    def _hash(self) -> int:
        return hash(tuple(self.predicates))

    def _stringify(self, indentation: int = 0) -> str:
        s = f"{self._indent(indentation)}<<CHAIN> [\n"
        for predicate in self.predicates:
            s += f"{predicate.stringify(indentation + 1)}\n"
        s += f"{self._indent(indentation)}]>"

        return s
