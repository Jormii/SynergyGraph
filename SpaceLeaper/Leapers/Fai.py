from predicates import *
from synergy_graph import IPredicate

from SpaceLeaper.predicates import *
from SpaceLeaper.leaper import Leaper
from SpaceLeaper.actions import Actions
from SpaceLeaper.subjects import Subjects

BOILING_CHANCE = 1 / 5


class Fai(Leaper):

    def __init__(self) -> None:
        super().__init__(
            self.__class__.__name__,
            Leaper.Class.HUNTER,
            Leaper.Element.FLAME,
            Leaper.EnergyOrb.THREE
        )

    def basic_attack(self) -> IPredicate:
        return DealDamage(
            self, Subjects.ENEMY, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 90)

    def talent(self) -> IPredicate:
        return Chance(
            DealDamage(
                self, Subjects.ENEMIES, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 250),
            BOILING_CHANCE
        )

    def character_gear(self) -> IPredicate:
        return Multiplier(self.basic_attack(), 50)

    def energy_skill(self) -> IPredicate:
        return DealDamage(
            self, Subjects.ENEMIES, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 190)

    def ultra_skill(self) -> IPredicate:
        return Repeat(
            DealDamage(
                self, Subjects.ENEMIES, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 90),
            4
        )
