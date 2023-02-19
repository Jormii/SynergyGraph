from predicates import *
from synergy_graph import SynergyGraph

from SpaceLeaper.leaper import Leaper
import SpaceLeaper.actions as sl_actions
import SpaceLeaper.subjects as sl_subjects


class Doranana(Leaper):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def _add_basic_attack(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
            factor=0.7
        ))

    def _add_talent(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Conditional(
            Witness(sl_subjects.ENEMY, sl_actions.ATTACK, self),
            Multiplier(
                Chain([
                    Execute(
                        sl_subjects.LULU, sl_actions.ENRAGE, sl_subjects.ENEMY),
                    Execute(
                        sl_subjects.LULU, sl_actions.LEVITATE, sl_subjects.ENEMY),
                    Multiplier(
                        Execute(
                            sl_subjects.LULU, sl_actions.ATK_INCREASE, sl_subjects.LULU),
                        factor=5 * 0.15
                    ),
                    Multiplier(
                        Execute(
                            sl_subjects.LULU, sl_actions.ATK_SPEED_INCREASE, sl_subjects.LULU),
                        factor=5 * 0.3
                    )
                ]),
                factor=1/8
            )
        ))

    def _add_character_gear(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.ENERGY_CRYSTAL_GAIN, self),
            factor=2
        ))
        graph.add_predicate(Multiplier(
            Multiplier(
                Chain([
                    Witness(
                        sl_subjects.LULU, sl_actions.CURRENT_HEALTH, sl_subjects.LULU),
                    Execute(
                        sl_subjects.LULU, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMIES_MELEE_RANGE),
                ]),
                factor=0.02
            )
        ))

    def _add_energy_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
            factor=0.5 * 1.82
        ))
        graph.add_predicate(Multiplier(
            Execute(self, sl_actions.DEAL_ENERGY_DMG, sl_subjects.ENEMY),
            factor=0.5 * 2
        ))

    def _add_ultra_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Chain([
            Execute(self, sl_actions.SUMMON, sl_subjects.LULU),
            Execute(sl_subjects.LULU, sl_actions.SHIELD, sl_subjects.LULU),
            Execute(
                sl_subjects.LULU, sl_actions.LEVITATE, sl_subjects.ENEMIES_MELEE_RANGE),
            Execute(
                sl_subjects.LULU, sl_actions.ENRAGE, sl_subjects.ENEMIES_MELEE_RANGE),
        ]))
        graph.add_predicate(Chain([
            Execute(sl_subjects.LULU, sl_actions.HEAL, sl_subjects.LULU),
            Multiplier(
                Execute(
                    sl_subjects.LULU, sl_actions.ATK_INCREASE, sl_subjects.LULU),
                factor=5 * 0.4
            )
        ]))

    def _add_ex_skill(self, graph: SynergyGraph) -> None:
        return super()._add_ex_skill(graph)
