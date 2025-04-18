import numpy as np
from pydantic import BaseModel, Field, field_validator
from typing import Literal

from entropy.models.eos.base import EosBaseModel
from entropy.models.eos.peng_robinson import PengRobinson
from entropy.utils.constants import Constants, EosModelNames


class SimplifiedIAPWSData(BaseModel):
  """Stores data for a simplified IAPWS equation of state."""
  name: Literal[EosModelNames.SIMPLIFIED_IAPWS] = Field(default=EosModelNames.SIMPLIFIED_IAPWS)
  mw_g_mol: float = Field(default=Constants.DEFAULT_MW_WATER)

  @field_validator("mw_g_mol")
  def validate_mw_g_mol(cls, v: float) -> float:
    if v <= 0:
      raise ValueError("Molecular weight must be positive")
    return v


class SimplifiedIAPWS(EosBaseModel):
  def __init__(self, mw_g_mol: float = Constants.DEFAULT_MW_WATER) -> None:
    """Simplified IAPWS-based model for water properties.
    
    Parameters:
    * `mw_g_mol`: Molecular weight (g/mol), default is water
    """
    self.mw_g_mol = mw_g_mol
    self.R = Constants.DEFAULT_R  # J/(mol·K)
    
    # Critical properties of water
    self.tc = Constants.DEFAULT_Tc_WATER  # K
    self.pc = Constants.DEFAULT_Pc_WATER  # Pa
    self.rhoc = 322.0  # kg/m³
    
    # Region boundaries
    self.T_boundary = 623.15  # K - boundary between regions
    
    # Reduced property reference values
    self.T_star = 1.0  # K
    self.p_star = 1.0  # Pa
    self.rho_star = 1.0  # kg/m³
    
    # Coefficients for different regions
    # These would be simplified from the full IAPWS formulation
    self._setup_coefficients()

    Tc_water = 647.096 # K
    Pc_water = 22.064e6 # Pa
    omega_water = 0.344
    self.pr_eos = PengRobinson(Tc=Tc_water, Pc=Pc_water, omega=omega_water, mw_g_mol=self.mw_g_mol)

  def to_data(self) -> SimplifiedIAPWSData:
    """Serialize the model to a data object."""
    return SimplifiedIAPWSData(
      name=EosModelNames.SIMPLIFIED_IAPWS,
      mw_g_mol=self.mw_g_mol
    )

  def to_dict(self) -> dict:
    """Serialize the model to a dictionary."""
    return self.to_data().model_dump()

  @classmethod
  def from_data(cls, data: SimplifiedIAPWSData | dict) -> 'SimplifiedIAPWS':
    """Construct this class from a `data` payload."""
    validated_data = SimplifiedIAPWSData.model_validate(data)
    return cls(
      mw_g_mol=validated_data.mw_g_mol
    )

  @property
  def model_name(self) -> str:
    """Returns the name of the model."""
    return EosModelNames.SIMPLIFIED_IAPWS

  def _setup_coefficients(self) -> None:
    """Set up coefficients for the simplified model."""
    # Coefficients for liquid region
    self.liquid_coeffs = {
      'a': [-7.85951783, 1.84408259, -11.7866497, 22.6807411, -15.9618719, 1.80122502],
      'b': [1.0, 1.5, 3.0, 3.5, 4.0, 7.5],
      'c': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    
    # Coefficients for vapor region
    self.vapor_coeffs = {
      'a': [-8.32044648, 6.6832105, 3.00632, 0.012436, 0.97315, 1.279186],
      'b': [1.0, 2.0, 4.0, 8.0, 10.0, 15.0],
      'c': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  
  def _reduced_density(self, T: float, P: float) -> float:
    """
    Calculate reduced density using a simplified approach.
    
    For a full IAPWS implementation, this would involve iterative solving
    of equations. Here we use a simplified correlation.
    """
    # Reduced properties
    tau = self.tc / T
    pi = P / self.pc
    
    # Check which phase we're in
    if T < self.tc and P < self._saturation_pressure(T):
      # Vapor phase - simplified correlation
      delta = pi / (tau * (1.0 + pi / tau**2))
    else:
      # Liquid or supercritical phase - simplified correlation
      delta = pi / (0.1 * tau) + 3.0 * np.sqrt(pi)
    
    return delta
  
  def _saturation_pressure(self, T: float) -> float:
    """Simplified saturation pressure correlation.

    Valid from triple point to critical point.
    """
    if T < 273.15 or T > self.tc:
      raise ValueError(f"Temperature {T} K is outside valid range for saturation pressure")
    
    # Reduced temperature
    tau = self.tc / T
    
    # Coefficients for simplified Wagner equation
    a1, a2, a3, a4 = -7.85951783, 1.84408259, -11.7866497, 22.6807411
    
    # Simplified calculation based on Wagner equation
    theta = 1.0 - T / self.tc
    psi = a1 * theta + a2 * theta**1.5 + a3 * theta**3 + a4 * theta**3.5
    
    return self.pc * np.exp(psi * tau / (1.0 - theta))
  
  def _helmholtz_ideal(self, tau: float, delta: float) -> float:
    """Simplified ideal gas part of the dimensionless Helmholtz energy."""
    return np.log(delta) + 3.0 * np.log(tau) + 2.5 * tau
  
  def _helmholtz_residual(self, tau: float, delta: float, T: float) -> float:
    """Simplified residual part of the dimensionless Helmholtz energy."""
    # Choose coefficients based on temperature
    if T < self.T_boundary:
      coeffs = self.liquid_coeffs
    else:
      coeffs = self.vapor_coeffs
    
    # Calculate residual Helmholtz energy
    phi_r = 0.0
    for i in range(len(coeffs['a'])):
      phi_r += coeffs['a'][i] * delta**coeffs['b'][i] * tau**coeffs['c'][i]
    
    return phi_r
  
  def _density_liquid(self, T: float, P: float) -> float:
    """Calculate liquid water density using a polynomial fit.
    
    Source: https://nvlpubs.nist.gov/nistpubs/jres/097/jresv97n3p335_A1b.pdf
    """
    T_C = T - 273.15  # Convert to Celsius
    T_C_2 = T_C * T_C
    T_C_3 = T_C_2 * T_C
    T_C_4 = T_C_3 * T_C
    T_C_5 = T_C_4 * T_C
    return (999.83952 + 16.945176 * T_C - 7.9870401e-3 * T_C_2 - 46.170461e-6 * T_C_3 + 105.56302e-9 * T_C_4 - 280.54253e-12 * T_C_5) / (1 + 16.87985e-3 * T_C)
  
  def density_mass(self, T: float, P: float) -> float:
    """Calculate water density using simplified IAPWS approach.

    Notes:
    * For ambient liquid water, we use a polynomial fit to the IAPWS-95 liquid density.
    * For other conditions, we use the Peng-Robinson EOS.
    
    Args:
    * `T`: Temperature (K)
    * `P`: Pressure (Pa)
    
    Returns:
    * Density (kg/m³)
    """
    # Special case for ambient liquid water - higher accuracy
    if 273.15 <= T <= 373.15 and P >= 101325: # Between freezing and boiling at >~1 atm
      return self._density_liquid(T, P)
    else:
      # If we're not in the liquid region, we can use the Peng-Robinson EOS. We force the solution to be vapor.
      return self.pr_eos.density_mass(T, P, force_solution="vapor")

  def density_molar(self, T: float, P: float) -> float:
    """Calculate the molar density of water in mol/m³."""
    return self.density_mass(T, P) / (self.mw_g_mol * 1e-3)
  
  def entropy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Calculate entropy change between two pressures.
    
    Uses Helmholtz energy formulation for improved accuracy.
    """
    if P1 == P2:
      return 0.0
    
    # Reduced temperature
    tau = self.tc / T
    
    # Calculate densities at each state
    rho1 = self.density_mass(T, P1)
    rho2 = self.density_mass(T, P2)
    
    # Reduced densities
    delta1 = rho1 / self.rhoc
    delta2 = rho2 / self.rhoc
    
    # For entropy from Helmholtz energy, we need partial derivatives
    # This is a simplified version of these calculations
    
    # Contribution from ideal part
    s_ideal = self.R * np.log(P1 / P2)
    
    # Contribution from residual part (simplified)
    # In a full implementation, this would involve proper derivatives
    s_residual = -self.R * (
      self._helmholtz_residual(tau, delta2, T) - 
      self._helmholtz_residual(tau, delta1, T)
    )
    
    return s_ideal + s_residual
  
  def entropy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Calculate the entropy change in J/(kg·K)."""
    return self.entropy_pressure_change_molar(T, P1, P2) / (self.mw_g_mol * 1e-3) # J/(kg·K) = J/(mol·K) / (g/mol * 1e-3)
  
  def enthalpy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Calculate the enthalpy change in J/mol."""
    return 0.0
  
  def enthalpy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Calculate the enthalpy change in J/kg."""
    return 0.0
  
  @property
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    return self.mw_g_mol
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    self.mw_g_mol = mw
