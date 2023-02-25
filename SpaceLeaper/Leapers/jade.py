from predicates import *
from synergy_graph import SynergyGraph

from SpaceLeaper.leaper import Leaper
import SpaceLeaper.actions as sl_actions
import SpaceLeaper.subjects as sl_subjects


class Jade(Leaper):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def _add_basic_attack(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.ATTACK, sl_subjects.ENEMY),
            factor=0.9,
            annotation="Jade Basic Attacks for 90% Physical DMG"
        ))

    def _add_talent(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Chain(
            [
                Multiplier(
                    Execute(self, sl_actions.ATK_INCREASE, sl_subjects.ALLY),
                    factor=0.3
                ),
                Multiplier(
                    Execute(
                        self, sl_actions.ATK_SPEED_INCREASE, sl_subjects.ALLY),
                    factor=0.35
                )
            ],
            annotation="Jade increases the ATK and ATK Speed of an ally by 30% and 35%"
        ))

    def _add_character_gear(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DMG_INCREASE, sl_subjects.HUNTER),
            factor=0.3,
            annotation="Jade increases the attack of Hunter allies attacking her target"
        ))

    def _add_energy_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Chain(
            [
                Multiplier(
                    Execute(self, sl_actions.LOSE_AGGRO, self),
                    factor=8
                ),
                Execute(self, sl_actions.HEAL, self)
            ],
            annotation="Jade loses aggro for 8 seconds and recovers 100% ATK Health"
        ))

    def _add_ultra_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Conditional(
                Witness(self, sl_actions.ATTACK, sl_subjects.ENEMY),
                Multiplier(
                    Execute(self, sl_actions.DEF_DECREASE, sl_subjects.ENEMY),
                    factor=0.3
                )
            ),
            factor=9,
            annotation="Jade's Basic Attacks pierce her target's DEF by 30% for 9 seconds"
        ))

    def _add_ex_skill(self, graph: SynergyGraph) -> None:
        return super()._add_ex_skill(graph)
