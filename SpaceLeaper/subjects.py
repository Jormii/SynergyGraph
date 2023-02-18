from typing import List

from synergy_graph import SynergyGraph
from subject import Subject, SubjectTag
from SpaceLeaper.leaper import Leaper
from SpaceLeaper.Leapers import (
    latika
)

ENEMY = Subject("Enemy", SubjectTag.ANY)

LATIKA = latika.Latika()


def create_synergy_graph() -> SynergyGraph:
    graph = SynergyGraph()

    # Leapers
    leapers: List[Leaper] = [
        LATIKA
    ]

    for leaper in leapers:
        leaper.add_to_graph(graph)

    # Is-a-relationships

    return graph
