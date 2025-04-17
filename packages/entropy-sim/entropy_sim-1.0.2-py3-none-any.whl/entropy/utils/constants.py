from enum import Enum


class Constants:
  """Global constants for the package."""
  DEFAULT_T_REF = 298.15 # NIST standard temperature (NTP)
  DEFAULT_P_REF = 101325 # NIST standard pressure (NTP)
  DEFAULT_MW_WATER = 18.01528 # g/mol

  # Gas constant (J/(mol·K))
  DEFAULT_R = 8.3144598 # J/(mol·K)

  # Peng-Robinson parameters
  DEFAULT_Tc_WATER = 647.096 # K
  DEFAULT_Pc_WATER = 22.064e6 # Pa
  DEFAULT_OMEGA_WATER = 0.344


class EosModelNames(str, Enum):
  """Names of the equation of state models."""
  CONSTANT_VOLUME = "constant_volume"
  IDEAL_GAS = "ideal_gas"
  PENG_ROBINSON = "peng_robinson"
  SIMPLIFIED_IAPWS = "simplified_iapws"


class HeatCapacityModelNames(str, Enum):
  """Names of the heat capacity models."""
  CONSTANT = "constant"
  NASA7 = "nasa_7"
  NASA9 = "nasa_9"
  SHOMATE = "shomate"