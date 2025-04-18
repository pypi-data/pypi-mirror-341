import numpy as np
from typing import List, Literal

from pydantic import BaseModel, Field, model_validator, field_validator

from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.models.heat_capacity.thermo_interval import ThermoInterval
from entropy.utils.constants import Constants, HeatCapacityModelNames


class NASABaseHeatCapacityData(BaseModel):
  """Base data class for NASA polynomial heat capacity models."""
  name: Literal[HeatCapacityModelNames.NASA7, HeatCapacityModelNames.NASA9]
  mw_g_mol: float
  intervals: List[ThermoInterval]

  @field_validator("mw_g_mol")
  def validate_mw_g_mol(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Molecular weight must be positive")
    return v


class NASA7HeatCapacityData(NASABaseHeatCapacityData):
  """Stores data for a NASA-7 polynomial heat capacity model."""
  name: Literal[HeatCapacityModelNames.NASA7] = Field(default=HeatCapacityModelNames.NASA7)

  @model_validator(mode="after")
  def check_n_intervals(cls, data: 'NASA7HeatCapacityData'):
    """Check that the number of intervals is correct and that each interval has the correct number of coefficients."""
    if len(data.intervals) == 0:
      raise ValueError("Must provide at least one interval")
    for interval in data.intervals:
      if len(interval.coeffs) != 7:
        raise ValueError("Each interval must have 7 coefficients.")
    return data


class NASA9HeatCapacityData(NASABaseHeatCapacityData):
  """Stores data for a NASA-9 polynomial heat capacity model."""
  name: Literal[HeatCapacityModelNames.NASA9] = Field(default=HeatCapacityModelNames.NASA9)

  @model_validator(mode="after")
  def check_n_intervals(cls, data: 'NASA9HeatCapacityData'):
    """Check that the number of intervals is correct and that each interval has the correct number of coefficients."""
    if len(data.intervals) == 0:
      raise ValueError("Must provide at least one interval")
    for interval in data.intervals:
      if len(interval.coeffs) != 9:
        raise ValueError("Each interval must have 9 coefficients.")
    return data


class NASABaseHeatCapacity(HeatCapacityBaseModel):
  """Base class for NASA polynomial heat capacity models."""
  
  def __init__(
    self,
    intervals: List[ThermoInterval],
    mw_g_mol: float | None = None,
  ) -> None:
    """Initialize the NASA heat capacity model.
    
    Args:
    * `intervals`: List of temperature intervals with their corresponding coefficients
    * `mw_g_mol`: Molecular weight of the substance (g/mol)

    Note that the temperature ranges do not have to be ordered.
    """
    super().__init__()
    if len(intervals) == 0:
      raise ValueError("Must provide at least one interval")

    if mw_g_mol is None:
      raise ValueError("Molecular weight must be provided")
    
    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")
    
    self._intervals = intervals
    self._mw_g_mol = mw_g_mol
    
  def _get_coefficients(self, T: float) -> List[float]:
    """Returns the appropriate coefficient set for the given temperature."""
    for interval in self._intervals:
      if interval.T_min <= T <= interval.T_max:
        return interval.coeffs
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
  def __init__(self, intervals: List[ThermoInterval], mw_g_mol: float | None = None) -> None:
    super().__init__(intervals, mw_g_mol)
  
  def to_data(self) -> NASA7HeatCapacityData:
    """Serialize the model to a data object."""
    return NASA7HeatCapacityData(
      name=HeatCapacityModelNames.NASA7,
      intervals=self._intervals,
      mw_g_mol=self._mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()

  @classmethod
  def from_data(cls, data: NASA7HeatCapacityData | dict) -> 'NASA7HeatCapacity':
    """Construct this class from a `data` payload."""
    validated_data = NASA7HeatCapacityData.model_validate(data)
    return cls(
      intervals=validated_data.intervals,
      mw_g_mol=validated_data.mw_g_mol
    )
  
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
  
  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self._mw_g_mol

  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self._mw_g_mol = mw


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
  def __init__(self, intervals: List[ThermoInterval], mw_g_mol: float | None = None) -> None:
    super().__init__(intervals, mw_g_mol)
  
  def to_data(self) -> NASA9HeatCapacityData:
    """Serialize the model to a data object."""
    return NASA9HeatCapacityData(
      name=HeatCapacityModelNames.NASA9,
      intervals=self._intervals,
      mw_g_mol=self._mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()

  @classmethod
  def from_data(cls, data: NASA9HeatCapacityData | dict) -> 'NASA9HeatCapacity':
    """Construct this class from a `data` payload."""
    validated_data = NASA9HeatCapacityData.model_validate(data)
    return cls(
      intervals=validated_data.intervals,
      mw_g_mol=validated_data.mw_g_mol
    )
    
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

  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self._mw_g_mol = mw
