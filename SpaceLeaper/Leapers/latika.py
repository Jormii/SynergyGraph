from predicates import *
from synergy_graph import SynergyGraph

from SpaceLeaper.leaper import Leaper
import SpaceLeaper.actions as sl_actions
import SpaceLeaper.subjects as sl_subjects


class Latika(Leaper):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def _add_basic_attack(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
            factor=0.9
        ))

    def _add_talent(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions, sl_subjects.ENEMY),
            factor=0.5 * 1.25
        ))

        graph.add_predicate(Conditional(
            Witness(self, sl_actions.TIME_PASS, self),
            Multiplier(
                Execute(self, sl_actions.CRIT_CHANCE_INCREASE, self),
                factor=1/3 * 0.02
            )
        ))

    def _add_character_gear(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Conditional(
            Witness(self, sl_actions.TIME_PASS, self),
            Multiplier(
                Execute(self, sl_actions.ATK_INCREASE, self),
                factor=1/3 * 0.2
            )
        ))

    def _add_energy_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
            factor=0.5 * 1.15
        ))

        graph.add_predicate(Conditional(
            Witness(self, sl_actions.MISSING_HEALTH, sl_subjects.ENEMY),
            Multiplier(
                Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
                factor=0.5 * 0.1
            )
        ))

    def _add_ultra_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
            factor=0.5 * 3.2
        ))
        graph.add_predicate(Conditional(
            Witness(self, sl_actions.MISSING_HEALTH, sl_subjects.ENEMY),
            Multiplier(
                Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
                factor=0.5 * 0.07
            )
        ))
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.HEAL, self),
            factor=0.5 * 0.2
        ))

    def _add_ex_skill(self, graph: SynergyGraph) -> None:
        return super()._add_ex_skill(graph)
