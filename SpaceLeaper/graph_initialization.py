from predicates import *
from synergy_graph import IPredicate, SynergyGraph

import SpaceLeaper.actions as sl_actions
import SpaceLeaper.subjects as sl_subjects
from SpaceLeaper.leaper import Leaper


def create_synergy_graph() -> SynergyGraph:
    graph = SynergyGraph()

    for leaper in sl_subjects.LEAPERS.values():
        graph.add_synonym(leaper, sl_subjects.ALLY)
        for skill in Leaper.Skill:
            graph.add_predicate(_skill_cast(leaper, skill))

    # Is-a-relationships

    return graph


def _skill_cast(leaper: Leaper, skill: Leaper.Skill) -> IPredicate:
    return Chain(
        [
            _cast_predicate(leaper, skill),
            leaper.skills_predicate(skill)
        ],
        annotation=f"{leaper.name}'s {skill.name}"
    )


def _cast_predicate(leaper: Leaper, skill: Leaper.Skill) -> IPredicate:
    if skill == Leaper.Skill.BASIC_ATTACK:
        return Execute(leaper, sl_actions.CAST, sl_subjects.BASIC_ATTACK)
    elif skill == Leaper.Skill.TALENT:
        return Execute(leaper, sl_actions.CAST, sl_subjects.TALENT)
    elif skill == Leaper.Skill.CHARACTER_GEAR:
        return Execute(leaper, sl_actions.CAST, sl_subjects.CHARACTER_GEAR)
    elif skill == Leaper.Skill.ENERGY_SKILL:
        return Multiplier(
            Execute(leaper, sl_actions.CAST, sl_subjects.ENERGY_SKILL),
            1000
        )
    elif skill == Leaper.Skill.ULTRA_SKILL:
        return Multiplier(
            Execute(leaper, sl_actions.CAST, sl_subjects.ULTRA_SKILL),
            1000 * leaper.energy_orbs.value
        )
    else:
        exit(f"Invalid Leaper.Skill \"{skill}\"")
