from predicates import *
from synergy_graph import IPredicate

from SpaceLeaper.predicates import *
from SpaceLeaper.leaper import Leaper
from SpaceLeaper.actions import Actions
from SpaceLeaper.subjects import Subjects


class BeckySD(Leaper):

    def __init__(self) -> None:
        super().__init__(
            self.__class__.__name__,
            Leaper.Class.SUPPORT,
            Leaper.Element.FLAME,
            Leaper.EnergyOrb.TWO
        )

    def basic_attack(self) -> IPredicate:
        return DealDamage(
            self, Subjects.ENEMY, Leaper.DamageType.ENERGY, Leaper.DamageArea.SINGLE, 125)

    def talent(self) -> IPredicate:
        buff = Chain([
            ModifyStat(
                self, Subjects.ALLY_HIGHEST_POWER, Leaper.Stat.ATTACK, Leaper.StatModification.INCREASE, 10),
            ModifyStat(
                self, Subjects.ALLY_HIGHEST_POWER, Leaper.Stat.HEALTH_RECOVERY, Leaper.StatModification.INCREASE, 30)
        ])

        buff_at_start = Duration(buff, 5, None, None)
        buff_after_start = Duration(buff, 5, None, 8)

        return Chain([Repeat(buff_at_start, 2), buff_after_start])

    def character_gear(self) -> IPredicate:
        # TODO
        return Chance(
            Heal(self, Subjects.ALLY_HIGHEST_POWER, 10, Leaper.Stat.MAX_HEALTH),
            30
        )

    def energy_skill(self) -> IPredicate:
        return Chain([
            ModifyStat(
                self, Subjects.ALLY_HIGHEST_POWER, Leaper.Stat.SHIELD, Leaper.StatModification.INCREASE, 10),
            ModifyStat(
                self, Subjects.ALLY_HIGHEST_POWER, Leaper.Stat.ENERGY, Leaper.StatModification.INCREASE, 300),
            ModifyStat(
                self, Subjects.ALLY_HIGHEST_POWER, Leaper.Stat.MAX_HEALTH, Leaper.StatModification.INCREASE, 15),
        ])

    def ultra_skill(self) -> IPredicate:
        healing = Heal(self, Subjects.ALLY, 26, Leaper.Stat.ATTACK)
        return Chain([
            Repeat(healing, 4),
            Chance(healing, 4*100/8)  # TODO
        ])
