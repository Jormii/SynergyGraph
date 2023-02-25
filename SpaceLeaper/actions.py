from action import Action

ATTACK = Action("Attack")
DEAL_PHYSICAL_DMG = Action("DealPhysicalDMG")
DEAL_ENERGY_DMG = Action("DealEnergyDMG")

ATK_INCREASE = Action("ATKIncrease")
ATK_SPEED_INCREASE = Action("ATKSpeedIncrease")
CRIT_DMG_INCREASE = Action("CritDMGIncrease")
CRIT_CHANCE_INCREASE = Action("CritChanceIncrease")

ENERGY_GAIN = Action("EnergyGain")
ENERGY_CRYSTAL_GAIN = Action("EnergyCrystalGain")

HEAL = Action("Heal")
SHIELD = Action("Shield")
SUMMON = Action("Summon")
TIME_PASS = Action("TimePassed")
CURRENT_HEALTH = Action("CurrentHealth")    # TODO: Wrong
MISSING_HEALTH = Action("MissingHealth")

ENRAGE = Action("Enrage")
LEVITATE = Action("Levitate")
