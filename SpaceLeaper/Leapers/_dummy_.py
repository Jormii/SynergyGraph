from predicates import *
from synergy_graph import IPredicate

from SpaceLeaper.actions import *
from SpaceLeaper.subjects import *
from SpaceLeaper.predicates import *
from SpaceLeaper.leaper import Leaper


class ___LEAPERS_NAME___(Leaper):

    def __init__(self) -> None:
        super().__init__(
            self.__class__.name,
            Leaper.Class.PASS,
            Leaper.Element.PASS,
            Leaper.EnergyOrb.ONE
        )

    def basic_attack(self) -> IPredicate:
        return super().basic_attack()

    def talent(self) -> IPredicate:
        return super().talent()

    def character_gear(self) -> IPredicate:
        return super().character_gear()

    def energy_skill(self) -> IPredicate:
        return super().energy_skill()

    def ultra_skill(self) -> IPredicate:
        return super().ultra_skill()
