import numpy as np
from typing import List, Tuple

from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.utils.constants import Constants, HeatCapacityModelNames


class NASABaseHeatCapacity(HeatCapacityBaseModel):
  """Base class for NASA polynomial heat capacity models."""
  
  def __init__(
    self,
    coefficients: List[List[float]],
    temperature_ranges: List[Tuple[float, float]],
    mw_g_mol: float | None = None,
  ) -> None:
    """Initialize the NASA heat capacity model.
    
    Args:
    * `coefficients`: List of coefficient sets for different temperature ranges
    * `mw_g_mol`: Molecular weight of the substance (g/mol)
    * `temperature_ranges`: List of (T_min, T_max) tuples for each coefficient set

    Note that the temperature ranges do not have to be ordered.
    """
    super().__init__()
    if len(coefficients) != len(temperature_ranges):
      raise ValueError("Must provide temperature ranges for each coefficient set")

    if mw_g_mol is None:
      raise ValueError("Molecular weight must be provided")
    
    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")
    
    # Check that all coefficients are numbers:
    for coeff in coefficients:
      if not all(isinstance(c, (int, float)) for c in coeff):
        raise ValueError("All coefficients must be numbers")
      
    # Check that all temperature ranges are valid:
    for T_min, T_max in temperature_ranges:
      if T_min < 0:
        raise ValueError("Temperature ranges must be positive")
      if T_min >= T_max:
        raise ValueError("Temperature ranges must be valid")

    self._coefficients = coefficients
    self._temperature_ranges = temperature_ranges
    self._mw_g_mol = mw_g_mol
    
  def _get_coefficients(self, T: float) -> List[float]:
    """Returns the appropriate coefficient set for the given temperature."""
    for coeff, (T_min, T_max) in zip(self._coefficients, self._temperature_ranges):
      if T_min <= T <= T_max:
        return coeff
    raise ValueError(f"Temperature {T} K is outside all valid ranges")
  
  def cp_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant pressure (J/kg·K)."""
    return self.cp_molar(T) / (self._mw_g_mol * 1e-3)
  
  def cv_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant volume (J/mol·K).
    
    For simplicity, assumes Cv ≈ Cp. For more accuracy, this should be
    calculated using the relationship between Cp and Cv for the specific
    substance type (e.g., ideal gas, real gas, etc.).
    """
    return self.cp_molar(T)
  
  def cv_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant volume (J/kg·K)."""
    return self.cv_molar(T) / (self._mw_g_mol * 1e-3)
  
  def enthalpy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific enthalpy change between temperatures T1 and T2 (J/kg)."""
    return self.enthalpy_temperature_change_molar(T1, T2) / (self._mw_g_mol * 1e-3)

  def entropy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific entropy change between temperatures T1 and T2 (J/kg·K)."""
    return self.entropy_temperature_change_molar(T1, T2) / (self._mw_g_mol * 1e-3)

  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self._mw_g_mol


class NASA7HeatCapacity(NASABaseHeatCapacity):
  """NASA-7 polynomial heat capacity model.
  
  The NASA-7 polynomial expresses heat capacity and thermodynamic properties as:
  ```
  Cp/R = a1 + a2*T + a3*T^2 + a4*T^3 + a5*T^4
  H/(RT) = a1 + a2*T/2 + a3*T^2/3 + a4*T^3/4 + a5*T^4/5 + a6/T
  S/R = a1*ln(T) + a2*T + a3*T^2/2 + a4*T^3/3 + a5*T^4/4 + a7
  ```
  where R is the gas constant.
  """
  def __init__(self, coefficients: List[List[float]], temperature_ranges: List[Tuple[float, float]], mw_g_mol: float | None = None) -> None:
    super().__init__(coefficients, temperature_ranges, mw_g_mol)
    if len(coefficients[0]) != 7:
      raise ValueError("NASA-7 polynomial must have 7 coefficients")
  
  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return HeatCapacityModelNames.NASA7

  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    R = Constants.DEFAULT_R  # Gas constant in J/(mol·K)
    a1, a2, a3, a4, a5, *_ = self._get_coefficients(T)
    return R * (a1 + a2*T + a3*T**2 + a4*T**3 + a5*T**4)
  
  def enthalpy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar enthalpy change between temperatures T1 and T2 (J/mol)."""
    R = Constants.DEFAULT_R  # Gas constant in J/(mol·K)
    
    def H(T: float) -> float:
      a1, a2, a3, a4, a5, a6, _ = self._get_coefficients(T)
      return R * T * (a1 + a2*T/2 + a3*T**2/3 + a4*T**3/4 + a5*T**4/5 + a6/T)
      
    return H(T2) - H(T1)
  
  def entropy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar entropy change between temperatures T1 and T2 (J/mol·K)."""
    R = Constants.DEFAULT_R  # Gas constant in J/(mol·K)
    
    def S(T: float) -> float:
      a1, a2, a3, a4, a5, _, a7 = self._get_coefficients(T)
      return R * (a1*np.log(T) + a2*T + a3*T**2/2 + a4*T**3/3 + a5*T**4/4 + a7)
      
    return S(T2) - S(T1)


class NASA9HeatCapacity(NASABaseHeatCapacity):
  """NASA-9 polynomial heat capacity model.
  
  The NASA-9 polynomial expresses heat capacity and thermodynamic properties as:
  ```
  Cp/R = a1*T^-2 + a2*T^-1 + a3 + a4*T + a5*T^2 + a6*T^3 + a7*T^4
  H/(RT) = -a1*T^-2 + a2*ln(T)/T + a3 + a4*T/2 + a5*T^2/3 + a6*T^3/4 + a7*T^4/5 + a8/T
  S/R = -a1*T^-2/2 - a2*T^-1 + a3*ln(T) + a4*T + a5*T^2/2 + a6*T^3/3 + a7*T^4/4 + a9
  ```
  where R is the gas constant.
  """
  def __init__(self, coefficients: List[List[float]], temperature_ranges: List[Tuple[float, float]], mw_g_mol: float | None = None) -> None:
    super().__init__(coefficients, temperature_ranges, mw_g_mol)
    if len(coefficients[0]) != 9:
      raise ValueError("NASA-9 polynomial must have 9 coefficients")
    
  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return HeatCapacityModelNames.NASA9

  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    R = Constants.DEFAULT_R  # Gas constant in J/(mol·K)
    a1, a2, a3, a4, a5, a6, a7, *_ = self._get_coefficients(T)
    return R * (a1*T**-2 + a2*T**-1 + a3 + a4*T + a5*T**2 + a6*T**3 + a7*T**4)
  
  def enthalpy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar enthalpy change between temperatures T1 and T2 (J/mol)."""
    R = Constants.DEFAULT_R  # Gas constant in J/(mol·K)
    
    def H(T: float) -> float:
      a1, a2, a3, a4, a5, a6, a7, a8, _ = self._get_coefficients(T)
      return R * T * (-a1*T**-2 + a2*np.log(T)/T + a3 + a4*T/2 + 
              a5*T**2/3 + a6*T**3/4 + a7*T**4/5 + a8/T)
      
    return H(T2) - H(T1)
  
  def entropy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar entropy change between temperatures T1 and T2 (J/mol·K)."""
    R = Constants.DEFAULT_R  # Gas constant in J/(mol·K)
    
    def S(T: float) -> float:
      a1, a2, a3, a4, a5, a6, a7, _, a9 = self._get_coefficients(T)
      return R * (-a1*T**-2/2 - a2*T**-1 + a3*np.log(T) + a4*T + 
             a5*T**2/2 + a6*T**3/3 + a7*T**4/4 + a9)
      
    return S(T2) - S(T1)

  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self._mw_g_mol
