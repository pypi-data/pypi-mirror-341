from enum import Enum

class Phase(str, Enum):
  SOLID = "solid"
  LIQUID = "liquid"
  GAS = "gas"
  AQUEOUS = "aqueous"
