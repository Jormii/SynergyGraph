from typing import List

from subject import Subject
from synergy_graph import SynergyGraph
from SpaceLeaper.leaper import Leaper
from SpaceLeaper.Leapers import (
    # Stone
    jade,

    # Liquid

    # Flame

    # Wind
    grimes,

    # Order
    latika,

    # Chaos
    doranana
)

ALLY = Subject("Ally")
ENEMY = Subject("Enemy")
ENEMIES = Subject("Enemies")
ENEMIES_MELEE_RANGE = Subject("EnemiesInMeleeRange")

HUNTER = Subject("Hunter")

JADE = jade.Jade()
GRIMES = grimes.Grimes()
LATIKA = latika.Latika()
DORANANA = doranana.Doranana()

# Pets
LULU = Subject("Lulu")


def create_synergy_graph() -> SynergyGraph:
    graph = SynergyGraph()

    # Leapers
    leapers: List[Leaper] = [
        JADE,
        GRIMES,
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
