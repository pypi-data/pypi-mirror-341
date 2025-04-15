class EosBaseModel:
  """Base class for equation of state models."""
  def __init__(self) -> None:
    pass
  
  def density_mass(self, T: float, P: float) -> float:
    """Returns the density of the material in kg/m³."""
    raise NotImplementedError("Density mass calculation not implemented.")
  
  def density_molar(self, T: float, P: float) -> float:
    """Returns the density of the material in mol/m³."""
    raise NotImplementedError("Density molar calculation not implemented.")
  
  def entropy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Returns the entropy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/mol·K)."""
    raise NotImplementedError("Entropy pressure change calculation not implemented.")
  
  def entropy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Returns the entropy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/kg·K)."""
    raise NotImplementedError("Entropy pressure change calculation not implemented.")
  
  def enthalpy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Returns the enthalpy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/mol)."""
    raise NotImplementedError("Enthalpy pressure change calculation not implemented.")
  
  def enthalpy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Returns the enthalpy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/kg)."""
    raise NotImplementedError("Enthalpy pressure change calculation not implemented.")
  
  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    raise NotImplementedError("Model name calculation not implemented.")