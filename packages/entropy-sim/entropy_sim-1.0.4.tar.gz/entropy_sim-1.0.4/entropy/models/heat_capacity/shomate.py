import numpy as np
from typing import List, Literal

from pydantic import BaseModel, Field, model_validator, field_validator

from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.models.heat_capacity.thermo_interval import ThermoInterval
from entropy.utils.constants import HeatCapacityModelNames


class ShomateHeatCapacityData(BaseModel):
  """Stores data for a Shomate thermo model."""
  name: Literal[HeatCapacityModelNames.SHOMATE] = Field(default=HeatCapacityModelNames.SHOMATE)
  intervals: list[ThermoInterval]
  mw_g_mol: float

  @field_validator("mw_g_mol")
  def validate_mw_g_mol(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Molecular weight must be positive")
    return v

  @model_validator(mode="after")
  def check_n_intervals(cls, data: 'ShomateHeatCapacityData'):
    if len(data.intervals) == 0:
      raise ValueError("Must provide at least one interval")
    for interval in data.intervals:
      if len(interval.coeffs) != 8:
        raise ValueError("Each interval must have exactly 8 coefficients.")
    return data


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
    intervals: List[ThermoInterval],
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

    if len(intervals) == 0:
      raise ValueError("Must provide at least one interval")

    if mw_g_mol is None or not isinstance(mw_g_mol, (int, float)):
      raise ValueError("Molecular weight must be provided")
    
    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")
      
    self._intervals = intervals
    self._mw_g_mol = mw_g_mol

  def to_data(self) -> ShomateHeatCapacityData:
    """Serialize the model to a data object."""
    return ShomateHeatCapacityData(
      intervals=self._intervals,
      mw_g_mol=self._mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()
  
  @classmethod
  def from_data(cls, data: ShomateHeatCapacityData | dict) -> 'ShomateHeatCapacity':
    """Construct this class from a `data` payload."""
    validated_data = ShomateHeatCapacityData.model_validate(data)
    return cls(
      intervals=validated_data.intervals,
      mw_g_mol=validated_data.mw_g_mol
    )

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return HeatCapacityModelNames.SHOMATE
    
  def _get_coefficients(self, T: float) -> List[float]:
    """Returns the appropriate coefficient set for the given temperature."""
    for interval in self._intervals:
      if interval.T_min <= T <= interval.T_max:
        return interval.coeffs

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

  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self._mw_g_mol = mw
