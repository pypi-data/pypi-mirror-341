import numpy as np
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.utils.constants import HeatCapacityModelNames


class ConstantHeatCapacityData(BaseModel):
  """Stores data for a constant heat capacity model."""
  name: Literal[HeatCapacityModelNames.CONSTANT] = Field(default=HeatCapacityModelNames.CONSTANT)
  cp_J_mol_K: float
  mw_g_mol: float

  @model_validator(mode="after")
  def validate_data(self) -> 'ConstantHeatCapacityData':
    if self.cp_J_mol_K <= 0:
      raise ValueError("cp_J_mol_K must be positive")
    if self.mw_g_mol <= 0:
      raise ValueError("mw_g_mol must be positive")
    return self


class ConstantHeatCapacity(HeatCapacityBaseModel):
  """Heat capacity model with constant Cp and Cv values.
  
  This model assumes that heat capacities do not vary with temperature.
  """
  
  def __init__(self, cp_J_mol_K: float, mw_g_mol: float) -> None:
    """
    Initialize the constant heat capacity model.
    
    Args:
    * `cp_J_mol_K`: Molar heat capacity at constant pressure (J/mol·K)
    * `mw_g_mol`: Molecular weight of the substance (g/mol)
    """
    super().__init__()
    if cp_J_mol_K is None:
      raise ValueError("cp_J_mol_K must be provided")
    if mw_g_mol is None:
      raise ValueError("mw_g_mol must be provided")
    if mw_g_mol <= 0:
      raise ValueError("mw_g_mol must be positive")
    if cp_J_mol_K <= 0:
      raise ValueError("cp_J_mol_K must be positive")
    self._cp_J_mol_K = cp_J_mol_K
    self._mw_g_mol = mw_g_mol

  def to_data(self) -> ConstantHeatCapacityData:
    """Serialize the model to a data object."""
    return ConstantHeatCapacityData(
      name=HeatCapacityModelNames.CONSTANT,
      cp_J_mol_K=self._cp_J_mol_K,
      mw_g_mol=self._mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()

  @classmethod
  def from_data(cls, data: ConstantHeatCapacityData | dict) -> 'ConstantHeatCapacity':
    """Construct this class from a `data` payload."""
    validated_data = ConstantHeatCapacityData.model_validate(data)
    return cls(
      cp_J_mol_K=validated_data.cp_J_mol_K,
      mw_g_mol=validated_data.mw_g_mol
    )

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return HeatCapacityModelNames.CONSTANT
    
  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    return self._cp_J_mol_K
  
  def cp_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant pressure (J/kg·K)."""
    return self._cp_J_mol_K / (self._mw_g_mol * 1e-3)
  
  def cv_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant volume (J/mol·K).
    
    For ideal gases, Cv = Cp - R. Here we assume Cv = Cp for simplicity.
    """
    return self._cp_J_mol_K
  
  def cv_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant volume (J/kg·K)."""
    return self.cv_molar(T) / (self._mw_g_mol * 1e-3)
  
  def enthalpy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar enthalpy change between temperatures T1 and T2 (J/mol)."""
    return self.cp_molar(T1) * (T2 - T1)
  
  def enthalpy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific enthalpy change between temperatures T1 and T2 (J/kg)."""
    return self.enthalpy_temperature_change_molar(T1, T2) / (self._mw_g_mol * 1e-3)
  
  def entropy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar entropy change between temperatures T1 and T2 (J/mol·K).
    
    For constant heat capacity: ΔS = Cp * ln(T2/T1)
    """
    return self.cp_molar(T1) * np.log(T2 / T1)
  
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
