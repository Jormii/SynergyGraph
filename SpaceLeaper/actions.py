from action import Action
from SpaceLeaper.leaper import Leaper


class DealDamage(Action):

    def __init__(self, damage: Leaper.Damage) -> None:
        super().__init__(f"Deal {damage.name} DMG")


DEAL_PHYSICAL_DMG = DealDamage(Leaper.Damage.PHYSICAL)
DEAL_ENERGY_DMG = DealDamage(Leaper.Damage.ENERGY)
