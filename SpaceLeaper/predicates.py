from __future__ import annotations
from enum import IntEnum

from predicates import *
from action import Action
from subject import Subject
from synergy_graph import IPredicate

from SpaceLeaper.leaper import Leaper
from SpaceLeaper.actions import Actions
from SpaceLeaper.subjects import Subjects


class SkillCast:

    def predicate(leaper: Leaper, skill: Leaper.Skill) -> IPredicate:
        return Chain(
            [
                SkillCast._cast_predicate(leaper, skill),
                leaper.skills_predicate(skill)
            ]
        )

    def _cast_predicate(leaper: Leaper, skill: Leaper.Skill) -> IPredicate:
        if skill == Leaper.Skill.BASIC_ATTACK:
            return Execute(leaper, Actions.CAST, Subjects.BASIC_ATTACK)
        elif skill == Leaper.Skill.TALENT:
            return Execute(leaper, Actions.CAST, Subjects.TALENT)
        elif skill == Leaper.Skill.CHARACTER_GEAR:
            return Execute(leaper, Actions.CAST, Subjects.CHARACTER_GEAR)
        elif skill == Leaper.Skill.ENERGY_SKILL:
            return Multiplier(
                Execute(leaper, Actions.CAST, Subjects.ENERGY_SKILL),
                1000
            )
        elif skill == Leaper.Skill.ULTRA_SKILL:
            return Multiplier(
                Execute(leaper, Actions.CAST, Subjects.ULTRA_SKILL),
                1000 * leaper.energy_orbs.value
            )
        else:
            raise Exception(skill)


class DealDamage:

    class Action(Action):

        def __init__(self, type: DealDamage.Type) -> None:
            super().__init__(f"Deal_{type.name}_DMG")

    class Type(IntEnum):
        PHYSICAL = 0
        ENERGY = 1
        TRUE = 2

    def predicate(actor: Subject, objective: Subject, type: DealDamage.Type,
                  scaling: int) -> IPredicate:
        return Multiplier(
            Execute(actor, DealDamage.Action(type), objective),
            scaling
        )
