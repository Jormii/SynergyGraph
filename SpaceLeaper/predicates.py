from __future__ import annotations

from predicates import *
from action import Action
from subject import Subject
from synergy_graph import IPredicate

from SpaceLeaper.leaper import Leaper
from SpaceLeaper.actions import Actions
from SpaceLeaper.subjects import Subjects


class SlPredicate(IPredicate):

    def __init__(self, annotation: str) -> None:
        super().__init__(annotation)

        self._predicate: IPredicate = None

    def _P(self) -> IPredicate:
        raise NotImplementedError(type(self))

    def _get_predicate(self) -> IPredicate:
        if self._predicate is None:
            self._predicate = self._P()

        return self._predicate

    def actors(self) -> Set[Subject]:
        return self._get_predicate().actors()

    def objectives(self) -> Set[Subject]:
        return self._get_predicate().objectives()

    def actions(self) -> Set[Action]:
        return self._get_predicate().actions()

    def _traverse(self, graph: SynergyGraph, instance: Synergy.Instance, out_synergy: Synergy) -> List[Synergy.Instance]:
        return self._get_predicate()._traverse(graph, instance, out_synergy)

    def _equals(self, predicate: SlPredicate) -> bool:
        if not isinstance(predicate, SlPredicate):
            return False

        return self._get_predicate() == predicate._get_predicate()

    def _hash(self) -> int:
        return hash(self._get_predicate())

    def _stringify(self, indentation: int) -> str:
        return self._get_predicate()._stringify(indentation)


class SkillCast(SlPredicate):

    def __init__(self, leaper: Leaper, skill: Leaper.Skill) -> None:
        super().__init__(f"{leaper.name} casts {skill.name}")

        self.leaper = leaper
        self.skill = skill

    def _P(self) -> IPredicate:
        if self.skill == Leaper.Skill.BASIC_ATTACK:
            return Execute(self.leaper, Actions.CAST, Subjects.BASIC_ATTACK)
        elif self.skill == Leaper.Skill.TALENT:
            return Execute(self.leaper, Actions.CAST, Subjects.TALENT)
        elif self.skill == Leaper.Skill.CHARACTER_GEAR:
            return Execute(self.leaper, Actions.CAST, Subjects.CHARACTER_GEAR)
        elif self.skill == Leaper.Skill.ENERGY_SKILL:
            return Multiplier(
                Execute(self.leaper, Actions.CAST, Subjects.ENERGY_SKILL),
                1000
            )
        elif self.skill == Leaper.Skill.ULTRA_SKILL:
            return Multiplier(
                Execute(self.leaper, Actions.CAST, Subjects.ULTRA_SKILL),
                1000 * self.leaper.energy_orbs.value
            )
        else:
            raise Exception(self.skill)


class DealDamage(SlPredicate):

    def __init__(self, actor: Subject, objective: Subject, type: Leaper.DamageType,
                 area: Leaper.DamageArea, scaling: int) -> None:
        super().__init__(
            f"{actor.name} deals {scaling}% {type.name}({area.name}) DMG to {objective.name}")

        self.actor = actor
        self.objective = objective
        self.type = type
        self.area = area
        self.scaling = scaling

    def _P(self) -> IPredicate:
        return Multiplier(
            Chain([
                Execute(
                    self.actor, self.type.action(), self.objective),
                Execute(
                    self.actor, self.area.action(), self.objective)
            ]),
            self.scaling / 100
        )


class ModifyStat(SlPredicate):

    def __init__(self, actor: Subject, objective: Subject, stat: Leaper.Stat, modification: Leaper.StatModification, scaling: int) -> None:
        super().__init__(
            f"{actor.name} {modification.name} {objective.name}'s {stat.name} by {scaling}%")

        self.actor = actor
        self.objective = objective
        self.stat = stat
        self.scaling = scaling

    def _P(self) -> IPredicate:
        return Multiplier(
            Execute(self.actor, self.stat.action(), self.objective),
            self.scaling / 100
        )


class ApplyCondition(SlPredicate):

    def __init__(self, actor: Subject, objective: Subject, condition: Leaper.Condition) -> None:
        super().__init__(
            f"{actor.name} applies {condition.name} to {objective.name}")

        self.actor = actor
        self.objective = objective
        self.condition = condition

    def _P(self) -> IPredicate:
        return Execute(self.actor, self.condition.action(), self.objective)


class Chance(SlPredicate):

    def __init__(self, predicate: IPredicate, chance: float) -> None:
        super().__init__(f"With a {chance}% chance")

        self.predicate = predicate
        self.chance = chance

    def _P(self) -> IPredicate:
        return Multiplier(self.predicate, self.chance / 100)


class Duration(SlPredicate):

    def __init__(self, predicate: IPredicate, duration: float, tick: float = 1, cooldown: float = None) -> None:
        super().__init__(
            f"Applies for {duration} seconds every {tick} seconds. CD: {cooldown}")

        self.predicate = predicate
        self.duration = duration
        self.tick = tick
        self.cooldown = cooldown    # TODO

    def _P(self) -> IPredicate:
        return Multiplier(self.predicate, self.duration / self.tick)    # TODO
