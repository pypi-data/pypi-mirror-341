import numpy as np
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from entropy.models.eos.base import EosBaseModel
from entropy.utils.constants import Constants, EosModelNames


class InvalidCubicEquationRootsError(Exception):
  """Exception raised when the cubic equation has invalid roots."""
  def __init__(self, message: str, roots: np.ndarray):
    self.message = message
    self.roots = roots
    super().__init__(self.message)


class PengRobinsonData(BaseModel):
  """Stores data for the Peng-Robinson equation of state."""
  name: Literal[EosModelNames.PENG_ROBINSON] = Field(default=EosModelNames.PENG_ROBINSON)
  Tc: float = Field(default=Constants.DEFAULT_Tc_WATER)
  Pc: float = Field(default=Constants.DEFAULT_Pc_WATER)
  omega: float = Field(default=Constants.DEFAULT_OMEGA_WATER)
  mw_g_mol: float = Field(default=Constants.DEFAULT_MW_WATER)

  @field_validator("mw_g_mol")
  def validate_mw_g_mol(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Molecular weight must be positive")
    return v


class PengRobinson(EosBaseModel):
  def __init__(self, Tc: float, Pc: float, omega: float, mw_g_mol: float) -> None:
    """Peng-Robinson equation of state model.
    
    Parameters:
    * `Tc`: Critical temperature (K)
    * `Pc`: Critical pressure (Pa)
    * `omega`: Acentric factor (dimensionless)
    * `mw_g_mol`: Molecular weight (g/mol)
    """
    # Check bad inputs
    if Tc is None:
      raise ValueError("Critical temperature must be provided")
    if Pc is None:
      raise ValueError("Critical pressure must be provided")
    if omega is None:
      raise ValueError("Acentric factor must be provided")
    if mw_g_mol is None:
      raise ValueError("Molecular weight must be provided")
    if Tc <= 0:
      raise ValueError("Critical temperature must be positive")
    if Pc <= 0:
      raise ValueError("Critical pressure must be positive")
    if mw_g_mol <= 0:
      raise ValueError("Molecular weight must be positive")

    self.Tc = Tc
    self.Pc = Pc
    self.omega = omega
    self.R = Constants.DEFAULT_R  # J/(mol·K)
    self.mw_g_mol = mw_g_mol

    # Calculate a and b parameters
    self.a = 0.45724 * (self.R * self.Tc)**2 / self.Pc
    self.b = 0.07780 * self.R * self.Tc / self.Pc
    
    # Parameter for a(T)
    self.kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
  
  def to_data(self) -> PengRobinsonData:
    """Serialize the model to a data object."""
    return PengRobinsonData(
      name=EosModelNames.PENG_ROBINSON,
      Tc=self.Tc,
      Pc=self.Pc,
      omega=self.omega,
      mw_g_mol=self.mw_g_mol
    )
  
  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()
  
  @classmethod
  def from_data(cls, data: PengRobinsonData | dict) -> 'PengRobinson':
    """Construct this class from a `data` payload."""
    validated_data = PengRobinsonData.model_validate(data)
    return cls(
      Tc=validated_data.Tc,
      Pc=validated_data.Pc,
      omega=validated_data.omega,
      mw_g_mol=validated_data.mw_g_mol
    )

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return EosModelNames.PENG_ROBINSON

  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self.mw_g_mol
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self.mw_g_mol = mw

  def _a_t(self, T: float) -> float:
    """Calculate the `a` parameter as a function of temperature."""
    tr = T / self.Tc
    alpha = (1 + self.kappa * (1 - np.sqrt(tr)))**2
    return self.a * alpha
  
  def _calculate_fugacity(self, T: float, P: float, Z: float) -> float:
    """Calculate the fugacity coefficient."""
    a_t = self._a_t(T)
    A = a_t * P / (self.R * T)**2
    B = self.b * P / (self.R * T)
    
    # Fugacity coefficient formula for PR-EOS
    lnphi = Z - 1 - np.log(Z - B) - A/(2*np.sqrt(2)*B) * \
            np.log((Z + (1+np.sqrt(2))*B)/(Z + (1-np.sqrt(2))*B))
    
    return np.exp(lnphi) * P
  
  def density_mass(self, T: float, P: float, force_solution: Literal["liquid", "vapor"] = None) -> float:
    """Calculate the density of the material in kg/m³ using the Peng-Robinson equation of state.
    
    Args:
    * `T`: Temperature (K)
    * `P`: Pressure (Pa)
    
    Returns:
    * Density (kg/m³)

    Notes:
    * There could be multiple roots to the cubic equation.
    * If
    """
    Z = self._calculate_z_factor(T, P, force_solution)

    # Calculate molar volume
    v_m = Z * self.R * T / P # m³/mol
    
    # Convert to density using molecular weight
    return (self.mw_g_mol * 1e-3) / v_m # kg/m³ = (g/mol * 1e-3) / m³/mol
  
  def density_molar(self, T: float, P: float) -> float:
    """Calculate the molar density of the material in mol/m³ using the Peng-Robinson equation of state."""
    return self.density_mass(T, P) / (self.mw_g_mol * 1e-3) # mol/m³ = kg/m³ / (g/mol * 1e-3)
  
  def _calculate_z_factor(self, T: float, P: float, force_solution: Literal["liquid", "vapor"] | None = None) -> float:
    """Helper method to calculate Z factor using the appropriate root selection."""
    # Solve cubic equation for compressibility factor Z
    a_t = self._a_t(T)
    
    A = a_t * P / (self.R * T)**2
    B = self.b * P / (self.R * T)
    
    # Cubic equation coefficients
    coef = [1, -(1-B), (A-3*B**2-2*B), -(A*B-B**2-B**3)]
    
    # Find all roots
    roots = np.roots(coef)
    
    # Only consider real roots
    real_roots = roots[np.isreal(roots)].real
    
    # Select appropriate root based on phase behavior
    if len(real_roots) == 1:
      return real_roots[0]

    elif len(real_roots) == 3:
      if force_solution == "liquid":
        return np.min(real_roots)
      elif force_solution == "vapor":
        return np.max(real_roots)
      else:
        # For entropy calculation, we need to be consistent with the phase
        # selection used in density_mass
        Z_vapor = np.max(real_roots)
        Z_liquid = np.min(real_roots)

        # Calculate the fugacity of the vapor and liquid phases
        fugacity_vapor = P * Z_vapor
        fugacity_liquid = P * Z_liquid
        
        # Calculate the Gibbs free energy of the vapor and liquid phases
        g_vapor = fugacity_vapor * Z_vapor
        g_liquid = fugacity_liquid * Z_liquid
        
        # The phase with the lowest Gibbs free energy is the more stable phase
        return Z_vapor if g_vapor < g_liquid else Z_liquid
  
    else:
      # If something weird happens, just take the max root
      # This should be handled more carefully in production code
      raise InvalidCubicEquationRootsError(f"Unexpected number of real roots found ({len(real_roots)}).", roots)

  def entropy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Calculate the entropy change of the material when the pressure changes from P1 to P2 
    at a constant temperature T (J/mol·K).
    
    For a real gas using Peng-Robinson EOS, we need to account for the departure
    from ideal gas behavior.
    """
    # If pressures are the same, there's no entropy change
    if P1 == P2:
      return 0.0
    
    # Calculate Z factors for each state
    Z1 = self._calculate_z_factor(T, P1)
    Z2 = self._calculate_z_factor(T, P2)
    
    # Calculate the a parameter at this temperature
    a_t = self._a_t(T)
    
    # Calculate A and B parameters for both states
    A1 = a_t * P1 / (self.R * T)**2
    B1 = self.b * P1 / (self.R * T)
    
    A2 = a_t * P2 / (self.R * T)**2
    B2 = self.b * P2 / (self.R * T)
    
    # Calculate the departure function for entropy at each state
    # This is the non-ideal contribution to entropy
    S_departure1 = self.R * np.log(Z1 - B1) + \
                  self.R * A1/(2*np.sqrt(2)*B1) * \
                  np.log((Z1 + (1+np.sqrt(2))*B1)/(Z1 + (1-np.sqrt(2))*B1))
    
    S_departure2 = self.R * np.log(Z2 - B2) + \
                  self.R * A2/(2*np.sqrt(2)*B2) * \
                  np.log((Z2 + (1+np.sqrt(2))*B2)/(Z2 + (1-np.sqrt(2))*B2))
    
    # Ideal gas contribution to entropy change
    S_ideal = -self.R * np.log(P2/P1)
    
    # Total entropy change: ideal gas contribution + difference in departure functions
    return S_ideal + (S_departure2 - S_departure1)

  def entropy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Calculate the entropy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/kg·K)."""
    return self.entropy_pressure_change_molar(T, P1, P2) / (self.mw_g_mol * 1e-3) # J/(kg·K) = J/(mol·K) / (g/mol * 1e-3)
  
  def enthalpy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Calculate the enthalpy change of the material when the pressure changes from
    P1 to P2 at a given temperature T (J/mol).
    """
    if P1 == P2:
      return 0.0
    
    # Get Z factors (compressibility) at each state
    Z1 = self._calculate_z_factor(T, P1)
    Z2 = self._calculate_z_factor(T, P2)
    
    # Calculate temperature derivative of 'a' parameter
    da_dt = -0.5 * self.a * self.kappa * (1 + self.kappa*(1-np.sqrt(T/self.Tc))) / np.sqrt(T*self.Tc)
    
    # Departure function terms for each state
    h_departure1 = self.R * T * (Z1 - 1) + T * da_dt/(2*np.sqrt(2)*self.b) * \
                  np.log((Z1 + (1+np.sqrt(2))*self.b*P1/(self.R*T))/(Z1 + (1-np.sqrt(2))*self.b*P1/(self.R*T)))
    
    h_departure2 = self.R * T * (Z2 - 1) + T * da_dt/(2*np.sqrt(2)*self.b) * \
                  np.log((Z2 + (1+np.sqrt(2))*self.b*P2/(self.R*T))/(Z2 + (1-np.sqrt(2))*self.b*P2/(self.R*T)))
    
    return h_departure2 - h_departure1
  
  def enthalpy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Calculate the enthalpy change of the material when the pressure changes from
    P1 to P2 at a given temperature T (J/kg).
    """
    return self.enthalpy_pressure_change_molar(T, P1, P2) / (self.mw_g_mol * 1e-3) # J/kg = J/mol / (g/mol * 1e-3)
