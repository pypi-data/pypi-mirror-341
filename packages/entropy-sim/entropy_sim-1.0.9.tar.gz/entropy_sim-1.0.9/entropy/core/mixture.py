import numpy as np
from pint import Quantity
from pydantic import BaseModel, Field
from typing import Literal
from entropy.core.component import Component, ComponentData
from entropy.utils.unit_registry import Q_, ensure_units, serialize_quantity
from entropy.utils.math import safe_normalize


class ValueWithUnits(BaseModel):
  """A value with units."""
  value: float | int | None = Field(default=None)
  units: str | None = Field(default=None)


class MixtureData(BaseModel):
  """Data model for a mixture."""
  components: list[ComponentData] = Field(default_factory=list)
  mass_fractions: list[float] = Field(default_factory=list)
  mole_fractions: list[float] = Field(default_factory=list)
  T: ValueWithUnits | None = Field(default=None)
  P: ValueWithUnits | None = Field(default=None)
  density_mass: ValueWithUnits | None = Field(default=None)
  density_molar: ValueWithUnits | None = Field(default=None)
  cp_molar: ValueWithUnits | None = Field(default=None)
  cp_mass: ValueWithUnits | None = Field(default=None)
  h_molar: ValueWithUnits | None = Field(default=None)
  h_mass: ValueWithUnits | None = Field(default=None)
  s_molar: ValueWithUnits | None = Field(default=None)
  s_mass: ValueWithUnits | None = Field(default=None)
  u_molar: ValueWithUnits | None = Field(default=None)
  u_mass: ValueWithUnits | None = Field(default=None)
  g_molar: ValueWithUnits | None = Field(default=None)
  g_mass: ValueWithUnits | None = Field(default=None)
  v_molar: ValueWithUnits | None = Field(default=None)
  v_mass: ValueWithUnits | None = Field(default=None)
  invalid_fields: list[str] = Field(default_factory=list)


class Mixture:
  """A mixture of chemical components."""
  def __init__(
    self,
    components: list[Component],
    fractions: list[float] | np.ndarray,
    basis: Literal["mole", "mass"] = "mass",
  ):
    """Initialize a mixture.
    
    Args:
    * `components`: List of components
    * `fractions`: List of mole or mass fractions
    * `basis`: Basis of the fractions, either 'mole' or 'mass'
    """
    if basis not in ["mole", "mass"]:
      raise ValueError("Basis must be either 'mole' or 'mass'")
    
    if len(components) != len(fractions):
      raise ValueError("Number of components must match number of fractions")
    
    if len(fractions) > 0 and isinstance(fractions[0], (Q_, Quantity)):
      fractions = [frac.magnitude for frac in fractions]

    if basis == "mole":
      self._mole_fractions = np.array(fractions)
      self._mass_fractions = np.array([comp.mw * frac for comp, frac in zip(components, fractions)])
    else:
      self._mass_fractions = np.array(fractions)
      self._mole_fractions = np.array([frac / comp.mw for comp, frac in zip(components, fractions)])
    
    # Normalize fractions
    self._mole_fractions = safe_normalize(self._mole_fractions)
    self._mass_fractions = safe_normalize(self._mass_fractions)

    total_moles = np.sum(self._mole_fractions)
    total_mass = np.sum(self._mass_fractions)

    if len(components) > 0 and not np.isclose(total_moles, 1.0):
      raise ValueError("Mole fractions for a non-empty mixture must sum to 1.0")

    if len(components) > 0 and not np.isclose(total_mass, 1.0):
      raise ValueError("Mass fractions for a non-empty mixture must sum to 1.0")

    self._components = components
    self._T = None
    self._P = None
    self._cache = {}  # For caching calculated properties
    
  @property
  def T(self) -> Q_:
    """Return the temperature of the mixture in units of degrees Kelvin."""
    return self._T
  
  @T.setter
  def T(self, value: float | Q_):
    """Set the temperature of the mixture in units of degrees Kelvin."""
    converted = ensure_units(value, "K")
    if self._T != converted:
      self._T = converted
      self._cache.clear()  # Clear cache when temperature changes
  
  @property
  def P(self) -> Q_:
    """Return the pressure of the mixture in units of Pa."""
    return self._P
  
  @P.setter
  def P(self, value: float | Q_):
    """Set the pressure of the mixture in units of Pa."""
    converted = ensure_units(value, "Pa")
    if self._P != converted:
      self._P = converted
      self._cache.clear()  # Clear cache when pressure changes
  
  def _check_state_defined(self):
    """Check if the temperature and pressure are set."""
    if self._T is None or self._P is None:
      raise ValueError("Temperature (T) and pressure (P) must be set before calculating properties.")
  
  @property
  def mw(self) -> Q_:
    """Average molecular weight of mixture (g/mol)"""
    if 'mw' not in self._cache:
      mws = np.array([comp.mw for comp in self.components])
      self._cache['mw'] = ensure_units(np.sum(self.mole_fractions * mws), "g/mol")
    return self._cache['mw']
  
  @property
  def cp_molar(self) -> Q_:
    """Molar heat capacity of mixture (J/(mol·K))"""
    self._check_state_defined()
    if 'cp_molar' not in self._cache:
      T, _ = self._T.to("K").magnitude, self._P.to("Pa").magnitude
      cps = np.array([comp.cp_molar(T) for comp in self.components])
      self._cache['cp_molar'] = ensure_units(np.sum(self.mole_fractions * cps), "J/(mol·K)")
    return self._cache['cp_molar']
  
  @property
  def cp_mass(self) -> Q_:
    """Mass-based heat capacity of mixture (J/(kg·K))"""
    if self.cp_molar.magnitude == 0 or self.mw.magnitude == 0:
      return ensure_units(0, "J/(kg·K)")
    return ensure_units(self.cp_molar / self.mw, "J/(kg·K)")
  
  @property
  def cv_molar(self) -> Q_:
    """Molar heat capacity of mixture (J/(mol·K))"""
    return self.cp_molar
  
  @property
  def cv_mass(self) -> Q_:
    """Mass-based heat capacity of mixture (J/(kg·K))"""
    if self.cv_molar.magnitude == 0 or self.mw.magnitude == 0:
      return ensure_units(0, "J/(kg·K)")
    return ensure_units(self.cv_molar / self.mw, "J/(kg·K)")
  
  @property
  def h_molar(self) -> Q_:
    """Molar enthalpy of mixture (J/mol)"""
    self._check_state_defined()
    if 'h_molar' not in self._cache:
      T, P = self._T.to("K").magnitude, self._P.to("Pa").magnitude
      hs = np.array([comp.h_molar(T, P) for comp in self.components])
      self._cache['h_molar'] = ensure_units(np.sum(self.mole_fractions * hs), "J/mol")
    return self._cache['h_molar']
  
  @property
  def h_mass(self) -> Q_:
    """Mass-based enthalpy of mixture (J/kg)"""
    if self.h_molar.magnitude == 0 or self.mw.magnitude == 0:
      return ensure_units(0, "J/kg")
    return ensure_units(self.h_molar / self.mw, "J/kg")
  
  @property
  def s_molar(self) -> Q_:
    """Molar entropy of mixture (J/(mol·K))"""
    self._check_state_defined()
    if 's_molar' not in self._cache:
      T, P = self._T.to("K").magnitude, self._P.to("Pa").magnitude
      s_components = np.array([comp.s_molar(T, P) for comp in self.components])
      self._cache['s_molar'] = ensure_units(np.sum(self.mole_fractions * s_components), "J/(mol·K)")
    return self._cache['s_molar']
  
  @property
  def s_mass(self) -> Q_:
    """Mass-based entropy of mixture (J/(kg·K))"""
    if self.s_molar.magnitude == 0 or self.mw.magnitude == 0:
      return ensure_units(0, "J/(kg·K)")
    return ensure_units(self.s_molar / self.mw, "J/(kg·K)")
  
  @property
  def density_mass(self) -> Q_:
    """Density of mixture (kg/m³)"""
    self._check_state_defined()
    if 'density_mass' not in self._cache:
      # Volume mixing rule (simplified)
      T, P = self._T.to("K").magnitude, self._P.to("Pa").magnitude
      comp_m3_per_kg = np.array([comp.v_mass(T, P) for comp in self.components])
      mix_m3_per_kg = np.sum(self.mass_fractions * comp_m3_per_kg)
      if mix_m3_per_kg == 0:
        self._cache['density_mass'] = ensure_units(0, "kg/m³")
      else:
        self._cache['density_mass'] = ensure_units(1 / mix_m3_per_kg, "kg/m³")
    return self._cache['density_mass']
  
  @property
  def density_molar(self) -> Q_:
    """Molar density of mixture (mol/m³)"""
    if self.density_mass.magnitude == 0:
      return ensure_units(0, "mol/m³")
    return ensure_units(self.density_mass / self.mw, "mol/m³")
  
  @property
  def v_molar(self) -> Q_:
    """Molar volume of mixture (m³/mol)"""
    if self.density_molar.magnitude == 0:
      return ensure_units(0, "m³/mol")
    return ensure_units(1 / self.density_molar, "m³/mol")
  
  @property
  def v_mass(self) -> Q_:
    """Mass-based volume of mixture (m³/kg)"""
    if self.density_mass.magnitude == 0:
      return ensure_units(0, "m³/kg")
    return ensure_units(1 / self.density_mass, "m³/kg")

  @property
  def mass_fractions(self) -> np.ndarray:
    """Mass fractions of mixture"""
    return self._mass_fractions
  
  @property
  def mole_fractions(self) -> np.ndarray:
    """Mole fractions of mixture"""
    return self._mole_fractions
  
  @property
  def components(self) -> list[Component]:
    """Components of mixture"""
    return self._components
  
  @property
  def u_molar(self) -> Q_:
    """Molar internal energy of mixture (J/mol)"""
    # print("WARNING: u_molar is not implemented for mixtures")
    return Q_(0, "J/mol")
  
  @property
  def u_mass(self) -> Q_:
    """Mass-based internal energy of mixture (J/kg)"""
    # print("WARNING: u_mass is not implemented for mixtures")
    return Q_(0, "J/kg")

  @property
  def g_molar(self) -> Q_:
    """Molar Gibbs free energy of mixture (J/mol)"""
    # print("WARNING: g_molar is not implemented for mixtures")
    return Q_(0, "J/mol")
  
  @property
  def g_mass(self) -> Q_:
    """Mass-based Gibbs free energy of mixture (J/kg)"""
    # print("WARNING: g_mass is not implemented for mixtures")
    return Q_(0, "J/kg")
  
  @property
  def n_components(self) -> int:
    """Number of components in mixture"""
    return len(self.components)
  
  def copy(self) -> 'Mixture':
    """Return a copy of the mixture (deep copy)."""
    copy = Mixture(
      [comp.copy() for comp in self.components],
      self.mole_fractions.copy(),
      basis="mole",
    )
    if self.T is not None:
      copy.T = self.T
    if self.P is not None:
      copy.P = self.P
    return copy
  
  def to_data(self) -> MixtureData:
    """Serialize the mixture to a data object."""
    data = {
      "invalid_fields": [],
    }

    for property in ["T", "P", "density_mass", "density_molar", "cp_molar", "cp_mass", "h_molar", "h_mass", "s_molar", "s_mass", "u_molar", "u_mass", "g_molar", "g_mass", "v_molar", "v_mass"]:
      try:
        data[property] = serialize_quantity(getattr(self, property))
      except ValueError:
        data[property] = None
        data["invalid_fields"].append(property)

    data["components"] = [comp.to_data() for comp in self.components]
    data["mass_fractions"] = self.mass_fractions.tolist()
    data["mole_fractions"] = self.mole_fractions.tolist()

    print(data)

    return MixtureData.model_validate(data)
  
  def serialize(self) -> dict:
    """Serialize the mixture to a dictionary."""
    return self.to_data().model_dump()