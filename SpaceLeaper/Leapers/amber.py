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
        return DealDamage(
            self, Subjects.ENEMY, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 75)

    def talent(self) -> IPredicate:
        return Conditional(
            Execute(Subjects.ENEMY, Actions.ATTACK, self),
            Duration(
                ModifyStat(
                    self, Subjects.ENEMY, Leaper.Stat.ACCURACY, Leaper.StatModification.DECREASE, 35),
                5, cooldown=8
            )
        )

    def character_gear(self) -> IPredicate:
        return Conditional(
            Execute(self, Actions.ATTACK, Subjects.ENEMY),
            Chance(
                Chain([
                    DealDamage(
                        self, Subjects.ENEMY, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 220),
                    Duration(
                        ApplyCondition(
                            self, Subjects.ENEMY, Leaper.Condition.BLIND),
                        3
                    )
                ]),
                20
            )
        )

    def energy_skill(self) -> IPredicate:
        return Duration(
            DealDamage(
                self, Subjects.ENEMY, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.AOE, 47),
            5
        )

    def ultra_skill(self) -> IPredicate:
        return Duration(
            Chain([
                DealDamage(
                    self, Subjects.ENEMY, Leaper.DamageType.PHYSICAL, Leaper.DamageArea.SINGLE, 95),
                Chance(
                    ApplyCondition(
                        self, Subjects.ENEMY, Leaper.Condition.STUN),
                    35
                )
            ]),
            2.1, tick=0.3
        )
