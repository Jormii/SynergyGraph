from predicates import *
from synergy_graph import SynergyGraph

from SpaceLeaper.leaper import Leaper
import SpaceLeaper.actions as sl_actions
import SpaceLeaper.subjects as sl_subjects


class Grimes(Leaper):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def _add_basic_attack(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Repeat(
            Multiplier(
                Execute(
                    self, sl_actions.DEAL_PHYSICAL_DMG, sl_subjects.ENEMY),
                factor=0.5
            ),
            times=2,
            annotation="Grimes attacks twice for 50% Physical DMG each"
        ))

    def _add_talent(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Conditional(
            Multiplier(
                Execute(self, sl_actions.ATTACK, sl_subjects.ENEMY),
                factor=1/6,
                annotation="Every 6 basic attacks"
            ),
            Chain(
                [
                    Multiplier(
                        Execute(self, sl_actions.CRIT_CHANCE_INCREASE, self),
                        factor=0.1
                    ),
                    Multiplier(
                        Execute(self, sl_actions.ATK_SPEED_INCREASE, self),
                        factor=0.1
                    )
                ],
                annotation="Increases Grimes' atk speed and crit chance by 10%"
            )
            # TODO: Stacks
        ))

    def _add_character_gear(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Conditional(
            Multiplier(
                Execute(self, sl_actions.ATTACK, sl_subjects.ENEMY),
                factor=0.5,
                annotation="When Grimes attacks and with a 50% chance"
            ),
            Chain(
                [
                    Execute(
                        self, sl_actions.DEAL_PHYSICAL_DMG, sl_subjects.ENEMY),
                    Multiplier(
                        Execute(self, sl_actions.CRIT_CHANCE_INCREASE, self),
                        factor=0.1
                    ),
                    Multiplier(
                        Execute(self, sl_actions.ATK_SPEED_INCREASE, self),
                        factor=0.1
                    )
                ],
                annotation="She deals 2 times Basic Attack's DMG and increases Grimes' atk speed and crit chance by 10%"
            )
            # TODO: Stacks
        ))

    def _add_energy_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Chain(
            [
                Multiplier(
                    Execute(self, sl_actions.CRIT_DMG_INCREASE, self),
                    factor=6
                ),
                Multiplier(
                    Execute(self, sl_actions.ENERGY_GAIN, self),
                    factor=500
                )
            ],
            annotation="Grimes gains Crit DMG and 500 Energy points"
        ))

    def _add_ultra_skill(self, graph: SynergyGraph) -> None:
        graph.add_predicate(Multiplier(
            Repeat(
                Multiplier(
                    Execute(self, sl_actions.ATTACK, sl_subjects.ENEMY),
                    factor=0.6
                ),
                15
            ),
            factor=1/3,
            annotation="Fires 15 60% Physical DMG Basic Attacks across 3 seconds"
        ))

    def _add_ex_skill(self, graph: SynergyGraph) -> None:
        return super()._add_ex_skill(graph)
