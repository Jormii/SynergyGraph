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
    Amber,
    BeckySD

    # Wind
    # Order
    # Chaos
)

LEAPERS: List[Leaper] = {
    # Stone
    # Liquid
    # Flame
    Amber.Amber(),
    BeckySD.BeckySD()

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
    graph.add_synonym(Subjects.ALLY_HIGHEST_POWER, Subjects.ALLY)

    return graph
