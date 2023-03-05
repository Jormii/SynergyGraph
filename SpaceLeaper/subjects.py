from typing import Dict

from subject import Subject

from SpaceLeaper.leaper import Leaper
from SpaceLeaper.Leapers import (
    # Flame
    amber
)

# Unit-related
BASIC_ATTACK = Subject("BasicAttack")
TALENT = Subject("Talent")
CHARACTER_GEAR = Subject("CharacterGear")
ENERGY_SKILL = Subject("EnergySkill")
ULTRA_SKILL = Subject("UltraSkill")

# Leapers
LEAPERS: Dict[str, Leaper] = dict([(l.name, l) for l in [
    amber.Amber()
]])

# Pets

# Others
ALLY = Subject("Ally")
