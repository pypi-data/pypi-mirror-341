from typing import Literal

from pydantic import BaseModel, Field, field_validator

from entropy.models.eos.base import EosBaseModel
from entropy.utils.constants import EosModelNames


class ConstantVolumeData(BaseModel):
  """Stores data for a constant-volume equation of state."""
  name: Literal[EosModelNames.CONSTANT_VOLUME] = Field(default=EosModelNames.CONSTANT_VOLUME)
  density_kg_m3: float = Field(default=1000)
  mw_g_mol: float = Field(default=100)

  @field_validator("mw_g_mol")
  def validate_mw_g_mol(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Molecular weight must be positive")
    return v
  
  @field_validator("density_kg_m3")
  def validate_density_kg_m3(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Density must be positive")
    return v


class ConstantVolume(EosBaseModel):
  """Constant volume equation of state model.
  
  In this model, density remains constant regardless of temperature and pressure.
  This is a simplified model that can be useful for incompressible materials or
  for specific simulation scenarios where density changes are negligible.
  """
  def __init__(self, density_kg_m3: float, mw_g_mol: float):
    """Initialize the constant volume EOS model.
    
    Args:
    * `density_kg_m3`: Constant mass density value (kg/m³)
    * `mw_g_mol`: Molecular weight (g/mol)
    """
    super().__init__()

    if density_kg_m3 is None:
      raise ValueError("Density must be provided")

    if mw_g_mol is None:
      raise ValueError("Molecular weight must be provided")
    
    if density_kg_m3 <= 0:
      raise ValueError("Density must be positive")

    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")

    self.density_kg_m3 = density_kg_m3
    self.mw_g_mol = mw_g_mol

  def to_data(self) -> ConstantVolumeData:
    """Serialize the model to a data object."""
    return ConstantVolumeData(
      name=EosModelNames.CONSTANT_VOLUME,
      density_kg_m3=self.density_kg_m3,
      mw_g_mol=self.mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()

  @classmethod
  def from_data(cls, data: ConstantVolumeData | dict) -> 'ConstantVolume':
    """Construct this class from a `data` payload."""
    validated_data = ConstantVolumeData.model_validate(data)
    return cls(
      density_kg_m3=validated_data.density_kg_m3,
      mw_g_mol=validated_data.mw_g_mol
    )

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return EosModelNames.CONSTANT_VOLUME
    
  def density_mass(self, T: float, P: float):
    """Return the constant mass density regardless of temperature and pressure.
    
    Args:
    * `T`: Temperature (K) - not used, but included for interface consistency
    * `P`: Pressure (Pa) - not used, but included for interface consistency
      
    Returns:
    * Constant mass density value (kg/m³)
    """
    return self.density_kg_m3
  
  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self.mw_g_mol
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self.mw_g_mol = mw
  
  def density_molar(self, T: float, P: float):
    """Return the constant molar density regardless of temperature and pressure.
    
    Args:
    * `T`: Temperature (K) - not used, but included for interface consistency
    * `P`: Pressure (Pa) - not used, but included for interface consistency
      
    Returns:
    * Constant molar density value (mol/m³)
    """
    return self.density_kg_m3 / self.mw_g_mol * 1e3
  
  def entropy_pressure_change_molar(self, T: float, P1: float, P2: float):
    """Calculate entropy change when pressure changes at constant volume.
    
    For a purely constant volume model, entropy change due to pressure change is zero.
    In real materials this might not be true, but this is a simplification.
    
    Args:
    * `T`: Temperature (K)
    * `P1`: Initial pressure (Pa)
    * `P2`: Final pressure (Pa)
      
    Returns:
    * Zero entropy change (J/(kg·K))
    """
    return 0.0

  def entropy_pressure_change_mass(self, T: float, P1: float, P2: float):
    """Calculate entropy change when pressure changes at constant volume.
    
    For a purely constant volume model, entropy change due to pressure change is zero.
    In real materials this might not be true, but this is a simplification.
    """
    return 0.0

  def enthalpy_pressure_change_molar(self, T: float, P1: float, P2: float):
    """Calculate enthalpy change when pressure changes at constant volume.
    
    For a purely constant volume model, enthalpy change due to pressure change is zero.
    In real materials this might not be true, but this is a simplification.
    """
    return 0.0
  
  def enthalpy_pressure_change_mass(self, T: float, P1: float, P2: float):
    """Calculate enthalpy change when pressure changes at constant volume.
    
    For a purely constant volume model, enthalpy change due to pressure change is zero.
    In real materials this might not be true, but this is a simplification.
    """
    return 0.0
  