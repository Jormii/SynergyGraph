from typing import List

from synergy_graph import SynergyGraph

from SpaceLeaper.leaper import Leaper
from SpaceLeaper.subjects import Subjects
from SpaceLeaper.predicates import SkillCast

from SpaceLeaper.Leapers import (
    # Stone
    # Liquid
    # Flame
    amber

    # Wind
    # Order
    # Chaos
)

LEAPERS: List[Leaper] = {
    # Stone
    # Liquid
    # Flame
    amber.Amber()

    # Wind
    # Order
    # Chaos
}


def create_synergy_graph() -> SynergyGraph:
    graph = SynergyGraph()

    for leaper in LEAPERS:
        assert leaper in Subjects.LEAPERS, f"Unknown Leaper \"{leaper}\""

        graph.add_synonym(leaper, Subjects.ALLY)
        for skill in Leaper.Skill:
            predicate = SkillCast.predicate(leaper, skill)
            predicate.annotation = f"{leaper.name}'s {skill.name}"

            graph.add_predicate(predicate)

    # Is-a-relationships

    return graph
