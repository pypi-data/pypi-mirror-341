import numpy as np
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from entropy.models.eos.base import EosBaseModel
from entropy.utils.constants import Constants, EosModelNames


class IdealGasData(BaseModel):
  """Stores data for an ideal gas equation of state."""
  name: Literal[EosModelNames.IDEAL_GAS] = Field(default=EosModelNames.IDEAL_GAS)
  mw_g_mol: float = Field(default=100)

  @field_validator("mw_g_mol")
  def validate_mw_g_mol(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Molecular weight must be positive")
    return v


class IdealGas(EosBaseModel):
  """Ideal gas equation of state model.
  
  This model implements the ideal gas equation: PV = nRT
  It's suitable for gases at relatively low pressures and high temperatures
  where intermolecular forces are negligible.
  """
  def __init__(self, mw_g_mol: float, R: float = Constants.DEFAULT_R):
    """Initialize the ideal gas EOS model.
    
    Args:
    * `mw_g_mol`: Molecular weight (g/mol)
    * `R`: Gas constant (J/(mol·K)), defaults to 8.314 J/(mol·K)
    """
    super().__init__()

    if mw_g_mol is None:
      raise ValueError("Molecular weight must be provided")

    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")

    if R is None:
      raise ValueError("Gas constant must be provided")

    if R <= 0:
      raise ValueError("Gas constant must be positive")

    self.mw_g_mol = mw_g_mol
    self.R = R
  
  def to_data(self) -> IdealGasData:
    """Serialize the model to a data object."""
    return IdealGasData(
      name=EosModelNames.IDEAL_GAS,
      mw_g_mol=self.mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()

  @classmethod
  def from_data(cls, data: IdealGasData | dict) -> 'IdealGas':
    """Construct this class from a `data` payload."""
    validated_data = IdealGasData.model_validate(data)
    return cls(
      mw_g_mol=validated_data.mw_g_mol
    )

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return EosModelNames.IDEAL_GAS

  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self.mw_g_mol
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self.mw_g_mol = mw
    
  def density_mass(self, T: float, P: float) -> float:
    """Calculate the mass density of the material in kg/m³ using the ideal gas law.
    
    Args:
    * `T`: Temperature (K)
    * `P`: Pressure (Pa)
      
    Returns:
    * Mass density (kg/m³)
    """
    return (P * self.mw_g_mol * 1e-3) / (self.R * T)
  
  def density_molar(self, T: float, P: float) -> float:
    """Calculate the molar density of the material in mol/m³ using the ideal gas law.
    
    Args:
    * `T`: Temperature (K)
    * `P`: Pressure (Pa)
      
    Returns:
    * Molar density (mol/m³)
    """
    return P / (self.R * T)
  
  def entropy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Calculate the entropy change of the material when the pressure changes from
    P1 to P2 at a given temperature T (J/kg·K).
    
    For an ideal gas, the entropy change when pressure changes at constant temperature is:
    ΔS = -R * ln(P2/P1) per unit mass
    
    Args:
    * `T`: Temperature (K)
    * `P1`: Initial pressure (Pa)
    * `P2`: Final pressure (Pa)
      
    Returns:
    * Entropy change (J/(kg·K))
    """
    return -(self.R / self.mw_g_mol * 1e-3) * np.log(P2 / P1)

  def entropy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Calculate the entropy change of the material when the pressure changes from
    P1 to P2 at a given temperature T (J/mol·K).
    """
    return self.entropy_pressure_change_mass(T, P1, P2) / self.mw_g_mol * 1e-3

  def enthalpy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Calculate the enthalpy change of the material when the pressure changes from
    P1 to P2 at a given temperature T (J/mol).
    """
    return 0.0

  def enthalpy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Calculate the enthalpy change of the material when the pressure changes from
    P1 to P2 at a given temperature T (J/kg).
    """
    return 0.0
