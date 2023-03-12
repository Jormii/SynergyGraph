from __future__ import annotations
from enum import IntEnum, auto
from typing import Callable, Dict

from action import Action
from subject import Subject
from synergy_graph import IPredicate


class Leaper(Subject):

    class Class(IntEnum):
        TANK = auto()
        FIGHTER = auto()
        ASSASIN = auto()
        HUNTER = auto()
        MAGE = auto()
        SUPPORT = auto()

    class Element(IntEnum):
        STONE = auto()
        LIQUID = auto()
        FLAME = auto()
        WIND = auto()
        ORDER = auto()
        CHAOS = auto()

    class EnergyOrb(IntEnum):
        ONE = 1
        TWO = 2
        THREE = 3

    class Skill(IntEnum):
        BASIC_ATTACK = auto()
        TALENT = auto()
        CHARACTER_GEAR = auto()
        ENERGY_SKILL = auto()
        ULTRA_SKILL = auto()

    class DamageType(IntEnum):
        PHYSICAL = auto()
        ENERGY = auto()
        TRUE = auto()

        def action(self) -> Action:
            return Action(f"DealDMG_T[{self.name}]")

    class DamageArea(IntEnum):
        SINGLE = auto()
        AOE = auto()

        def action(self) -> Action:
            return Action(f"DealDMG_A[{self.name}]")

    class Stat(IntEnum):
        ACCURACY = auto()

        def action(self) -> Action:
            return Action(f"ModifyStat[{self.name}]")

    class StatModification(IntEnum):
        DECREASE = auto()
        INCREASE = auto()

    class Condition(IntEnum):
        BLIND = auto()
        STUN = auto()

        def action(self) -> Action:
            return Action(f"Apply[{self.name}]")

    def __init__(self, name: str, leaper_class: Leaper.Class, leaper_element: Leaper.Element,
                 energy_orbs: Leaper.EnergyOrb) -> None:
        super().__init__(name)

        self.leaper_class = leaper_class
        self.leaper_element = leaper_element
        self.energy_orbs = energy_orbs

    def skills_predicate(self, skill: Leaper.Skill) -> IPredicate:
        MAPPING: Dict[Leaper.Skill, Callable[[Leaper], IPredicate]] = {
            Leaper.Skill.BASIC_ATTACK: self.basic_attack,
            Leaper.Skill.TALENT: self.talent,
            Leaper.Skill.CHARACTER_GEAR: self.character_gear,
            Leaper.Skill.ENERGY_SKILL: self.energy_skill,
            Leaper.Skill.ULTRA_SKILL: self.ultra_skill
        }

        return MAPPING[skill]()

    def basic_attack(self) -> IPredicate:
        raise NotImplementedError(type(self))

    def talent(self) -> IPredicate:
        raise NotImplementedError(type(self))

    def character_gear(self) -> IPredicate:
        raise NotImplementedError(type(self))

    def energy_skill(self) -> IPredicate:
        raise NotImplementedError(type(self))

    def ultra_skill(self) -> IPredicate:
        raise NotImplementedError(type(self))
