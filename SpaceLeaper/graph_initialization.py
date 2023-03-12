from typing import List

from predicates import Chain
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
            graph.add_predicate(Chain(
                [
                    SkillCast(leaper, skill),
                    leaper.skills_predicate(skill)
                ],
                annotation=f"{leaper.name}'s {skill.name}"
            ))

    # Is-a-relationships

    return graph
