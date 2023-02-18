from predicates import *
from synergy_graph import SynergyGraph

from SpaceLeaper.leaper import Leaper
import SpaceLeaper.actions as sl_actions
import SpaceLeaper.subjects as sl_subjects


class A_LEAPER(Leaper):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def _add_basic_attack(self, graph: SynergyGraph) -> None:
        pass

    def _add_talent(self, graph: SynergyGraph) -> None:
        pass

    def _add_character_gear(self, graph: SynergyGraph) -> None:
        pass

    def _add_energy_skill(self, graph: SynergyGraph) -> None:
        pass

    def _add_ultra_skill(self, graph: SynergyGraph) -> None:
        pass

    def _add_ex_skill(self, graph: SynergyGraph) -> None:
        return super()._add_ex_skill(graph)
