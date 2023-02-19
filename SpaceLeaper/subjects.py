from typing import List

from synergy_graph import SynergyGraph
from subject import Subject, SubjectTag
from SpaceLeaper.leaper import Leaper
from SpaceLeaper.Leapers import (
    # Order
    latika,

    # Chaos
    doranana
)

ALLY = Subject("Ally", SubjectTag.ANY)
ENEMY = Subject("Enemy", SubjectTag.ANY)
ENEMIES = Subject("Enemies", SubjectTag.ANY)
ENEMIES_MELEE_RANGE = Subject("EnemiesInMeleeRange", SubjectTag.ANY)

LATIKA = latika.Latika()
DORANANA = doranana.Doranana()

# Pets
LULU = Subject("Lulu", SubjectTag.ANY)


def create_synergy_graph() -> SynergyGraph:
    graph = SynergyGraph()

    # Leapers
    leapers: List[Leaper] = [
        LATIKA,
        DORANANA
    ]

    for leaper in leapers:
        leaper.add_to_graph(graph)
        graph.add_synonym(leaper, ALLY)

    # Is-a-relationships
    graph.add_synonym(ENEMIES, ENEMY)
    graph.add_synonym(ENEMIES_MELEE_RANGE, ENEMIES)

    return graph
