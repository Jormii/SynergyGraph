from predicates import *
from synergy_graph import IPredicate

from SpaceLeaper.actions import *
from SpaceLeaper.subjects import *
from SpaceLeaper.predicates import *
from SpaceLeaper.leaper import Leaper


class Amber(Leaper):

    def __init__(self) -> None:
        super().__init__(
            self.__class__.__name__,
            Leaper.Class.PASS,
            Leaper.Element.PASS,
            Leaper.EnergyOrb.TWO
        )

    def basic_attack(self) -> IPredicate:
        return Execute(self, CAST, self)

    def talent(self) -> IPredicate:
        return Execute(self, CAST, self)

    def character_gear(self) -> IPredicate:
        return Execute(self, CAST, self)

    def energy_skill(self) -> IPredicate:
        return Execute(self, CAST, self)

    def ultra_skill(self) -> IPredicate:
        return Execute(self, CAST, self)
