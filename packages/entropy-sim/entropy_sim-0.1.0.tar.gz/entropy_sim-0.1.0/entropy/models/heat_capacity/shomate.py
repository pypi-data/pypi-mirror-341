import numpy as np
from typing import List, Tuple

from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.utils.constants import HeatCapacityModelNames


class ShomateHeatCapacity(HeatCapacityBaseModel):
  """Heat capacity model using the Shomate equation.
  
  The Shomate equation expresses heat capacity and thermodynamic properties as:
  ```
  Cp = A + B*t + C*t^2 + D*t^3 + E/t^2  (where t = T/1000)
  H = H_ref + A*t + B*t^2/2 + C*t^3/3 + D*t^4/4 - E/t + F - H
  S = A*ln(t) + B*t + C*t^2/2 + D*t^3/3 - E/(2*t^2) + G
  ```
  where t = T/1000.
  """
  def __init__(
    self,
    coefficients: List[float] | List[List[float]],
    temperature_ranges: List[Tuple[float, float]] | None = None,
    mw_g_mol: float | None = None,
  ) -> None:
    """
    Initialize the Shomate heat capacity model.
    
    Args:
    * `coefficients`: List of Shomate coefficients [A, B, C, D, E, F, G, H].
      Can be a list of lists for multiple temperature ranges.
    * `mw_g_mol`: Molecular weight of the substance (g/mol)
    * `temperature_ranges`: List of (T_min, T_max) tuples for each coefficient set.
      Required if multiple coefficient sets are provided.
    """
    super().__init__()

    if temperature_ranges is None:
      temperature_ranges = [(0, float('inf'))]

    if not isinstance(coefficients[0], (list, tuple)):
      coefficients = [coefficients]

    if mw_g_mol is None or not isinstance(mw_g_mol, (int, float)):
      raise ValueError("Molecular weight must be provided")
    
    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")
    
    # Check that all coefficients are numbers:
    for coeff in coefficients:
      for c in coeff:
        if not isinstance(c, (int, float)):
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

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return HeatCapacityModelNames.SHOMATE
    
  def _get_coefficients(self, T: float) -> List[float]:
    """Returns the appropriate coefficient set for the given temperature."""
    for coeff, (T_min, T_max) in zip(self._coefficients, self._temperature_ranges):
      if T_min <= T <= T_max:
        return coeff

    raise ValueError(f"Temperature {T} K is outside all valid ranges")
    
  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    t = T / 1000  # Shomate equations use t = T/1000
    A, B, C, D, E, *_ = self._get_coefficients(T)
    return A + B*t + C*t**2 + D*t**3 + E/(t**2)
  
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
  
  def enthalpy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar enthalpy change between temperatures T1 and T2 (J/mol)."""
    def H(T: float) -> float:
      t = T / 1000
      A, B, C, D, E, F, _, H = self._get_coefficients(T)
      return (A*t + B*t**2/2 + C*t**3/3 + D*t**4/4 - E/t + F - H) * 1000
      
    return H(T2) - H(T1)
  
  def enthalpy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific enthalpy change between temperatures T1 and T2 (J/kg)."""
    return self.enthalpy_temperature_change_molar(T1, T2) / (self._mw_g_mol * 1e-3)
  
  def entropy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar entropy change between temperatures T1 and T2 (J/mol·K)."""
    def S(T: float) -> float:
      t = T / 1000
      A, B, C, D, E, _, G, _ = self._get_coefficients(T)
      return A*np.log(t) + B*t + C*t**2/2 + D*t**3/3 - E/(2*t**2) + G
      
    return S(T2) - S(T1)
  
  def entropy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific entropy change between temperatures T1 and T2 (J/kg·K)."""
    return self.entropy_temperature_change_molar(T1, T2) / (self._mw_g_mol * 1e-3)

  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self._mw_g_mol
