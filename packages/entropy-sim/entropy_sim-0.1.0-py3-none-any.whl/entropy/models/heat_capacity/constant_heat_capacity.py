import numpy as np

from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.utils.constants import HeatCapacityModelNames


class ConstantHeatCapacity(HeatCapacityBaseModel):
  """Heat capacity model with constant Cp and Cv values.
  
  This model assumes that heat capacities do not vary with temperature.
  """
  
  def __init__(self, cp_molar: float, mw_g_mol: float) -> None:
    """
    Initialize the constant heat capacity model.
    
    Args:
    * `cp_molar`: Molar heat capacity at constant pressure (J/mol·K)
    * `mw_g_mol`: Molecular weight of the substance (g/mol)
    """
    super().__init__()
    if cp_molar is None:
      raise ValueError("cp_molar must be provided")
    if mw_g_mol is None:
      raise ValueError("mw_g_mol must be provided")
    if mw_g_mol <= 0:
      raise ValueError("mw_g_mol must be positive")
    if cp_molar <= 0:
      raise ValueError("cp_molar must be positive")
    self._cp_molar = cp_molar
    self._mw_g_mol = mw_g_mol

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return HeatCapacityModelNames.CONSTANT
    
  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    return self._cp_molar
  
  def cp_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant pressure (J/kg·K)."""
    return self._cp_molar / (self._mw_g_mol * 1e-3)
  
  def cv_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant volume (J/mol·K).
    
    For ideal gases, Cv = Cp - R. Here we assume Cv = Cp for simplicity.
    """
    return self._cp_molar
  
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
