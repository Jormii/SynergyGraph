from synergy_graph import SynergyGraph
from subject import Subject, SubjectTag


class Leaper(Subject):

    def __init__(self, name: str) -> None:
        super().__init__(name, SubjectTag.CHARACTER)

    def add_to_graph(self, graph: SynergyGraph, add_ex_skills: bool = False) -> None:
        self._add_basic_attack(graph)
        self._add_talent(graph)
        self._add_character_gear(graph)
        self._add_energy_skill(graph)
        self._add_ultra_skill(graph)
        if add_ex_skills:
            self._add_ex_skill(graph)

    def _add_basic_attack(self, graph: SynergyGraph) -> None:
        raise NotImplementedError(f"{type(self)}")

    def _add_talent(self, graph: SynergyGraph) -> None:
        raise NotImplementedError(f"{type(self)}")

    def _add_character_gear(self, graph: SynergyGraph) -> None:
        raise NotImplementedError(f"{type(self)}")

    def _add_energy_skill(self, graph: SynergyGraph) -> None:
        raise NotImplementedError(f"{type(self)}")

    def _add_ultra_skill(self, graph: SynergyGraph) -> None:
        raise NotImplementedError(f"{type(self)}")

    def _add_ex_skill(self, graph: SynergyGraph) -> None:
        raise NotImplementedError(f"{type(self)}")
