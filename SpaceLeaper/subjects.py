import os
from typing import List

from subject import Subject


def all_leapers_names() -> List[str]:
    names: List[str] = []

    files_dir, _ = os.path.split(__file__)
    leapers_dir = os.path.join(files_dir, "Leapers/")
    for filename in os.listdir(leapers_dir):
        path = os.path.join(leapers_dir, filename)
        if os.path.isfile(path):
            name, _ = os.path.splitext(filename)
            names.append(name)

    return names


class Subjects:

    # Unit-related
    BASIC_ATTACK = Subject("BasicAttack")
    TALENT = Subject("Talent")
    CHARACTER_GEAR = Subject("CharacterGear")
    ENERGY_SKILL = Subject("EnergySkill")
    ULTRA_SKILL = Subject("UltraSkill")

    # Leapers
    LEAPERS = set([Subject(name) for name in all_leapers_names()])

    # Pets

    # Others
    ALLY = Subject("Ally")
    ALLY_HIGHEST_POWER = Subject("AllyHighestPower")
    ENEMY = Subject("Enemy")
    ENEMIES = Subject("Enemies")
