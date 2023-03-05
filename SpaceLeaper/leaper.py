from __future__ import annotations
from enum import IntEnum
from typing import Callable, Dict

from subject import Subject
from synergy_graph import IPredicate


class Leaper(Subject):

    class Class(IntEnum):
        PASS = 0

    class Element(IntEnum):
        PASS = 0

    class EnergyOrb(IntEnum):
        ONE = 1
        TWO = 2
        THREE = 3

    class Skill(IntEnum):
        BASIC_ATTACK = 0
        TALENT = 1
        CHARACTER_GEAR = 2
        ENERGY_SKILL = 3
        ULTRA_SKILL = 4

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
