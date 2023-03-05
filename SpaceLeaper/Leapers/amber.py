from predicates import *
from synergy_graph import IPredicate

from SpaceLeaper.predicates import *
from SpaceLeaper.leaper import Leaper
from SpaceLeaper.actions import Actions
from SpaceLeaper.subjects import Subjects


class Amber(Leaper):

    def __init__(self) -> None:
        super().__init__(
            self.__class__.__name__,
            Leaper.Class.ASSASIN,
            Leaper.Element.FLAME,
            Leaper.EnergyOrb.TWO
        )

    def basic_attack(self) -> IPredicate:
        return DealDamage.predicate(self, Subjects.ENEMY, DealDamage.Type.PHYSICAL, 75)

    def talent(self) -> IPredicate:
        return Execute(self, Actions.CAST, self)

    def character_gear(self) -> IPredicate:
        return Execute(self, Actions.CAST, self)

    def energy_skill(self) -> IPredicate:
        return Execute(self, Actions.CAST, self)

    def ultra_skill(self) -> IPredicate:
        return Execute(self, Actions.CAST, self)
