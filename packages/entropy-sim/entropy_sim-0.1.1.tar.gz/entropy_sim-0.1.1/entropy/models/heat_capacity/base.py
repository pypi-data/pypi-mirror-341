class HeatCapacityBaseModel:
  """Base class for heat capacity models."""
  def __init__(self) -> None:
    pass
  
  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    raise NotImplementedError("Molar heat capacity at constant pressure calculation not implemented.")
  
  def cp_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant pressure (J/kg·K)."""
    raise NotImplementedError("Specific heat capacity at constant pressure calculation not implemented.")
  
  def cv_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant volume (J/mol·K)."""
    raise NotImplementedError("Molar heat capacity at constant volume calculation not implemented.")
  
  def cv_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant volume (J/kg·K)."""
    raise NotImplementedError("Specific heat capacity at constant volume calculation not implemented.")
  
  def enthalpy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar enthalpy change between temperatures T1 and T2 (J/mol)."""
    raise NotImplementedError("Molar enthalpy change calculation not implemented.")
  
  def enthalpy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific enthalpy change between temperatures T1 and T2 (J/kg)."""
    raise NotImplementedError("Specific enthalpy change calculation not implemented.")
  
  def entropy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar entropy change between temperatures T1 and T2 (J/mol·K)."""
    raise NotImplementedError("Molar entropy change calculation not implemented.")
  
  def entropy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific entropy change between temperatures T1 and T2 (J/kg·K)."""
    raise NotImplementedError("Specific entropy change calculation not implemented.")

  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    raise NotImplementedError("Molecular weight calculation not implemented.")

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    raise NotImplementedError("Model name calculation not implemented.")
