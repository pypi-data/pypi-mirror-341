from pydantic import BaseModel, Field

from entropy.models.eos.base import EosBaseModel
from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.utils.constants import Constants
from entropy.core.phase import Phase
from entropy.utils.unit_registry import Q_, ensure_units


class ComponentData(BaseModel):
  """Data model for a chemical component."""
  id: str
  name: str
  phase: Phase
  formula: dict[str, int | float] | None = Field(default=None)
  mw: float


class Component:
  """Base class for chemical components."""
  def __init__(
    self,
    id: str,
    name: str,
    phase: Phase,
    formula: dict[str, int | float] | None,
    mw: Q_ | float,
    heat_capacity_model: HeatCapacityBaseModel,
    eos_model: EosBaseModel
  ) -> None:
    """Initialize a chemical component.
    
    Args:
    * `id`: Unique identifier for the component
    * `name`: Name of the component
    * `phase`: Phase of the component
    * `formula`: Chemical formula of the component
    * `heat_capacity_model`: Heat capacity model
    * `eos_model`: Equation of state model
    """
    try:
      phase = Phase(phase)
    except ValueError:
      raise ValueError(f"Invalid phase for component {name}: {phase}")

    self.id = id
    self.name = name
    self.phase = phase
    self.formula = formula
    self.heat_capacity_model = heat_capacity_model
    self.eos_model = eos_model

    # Update the molecular weight to be consistent across all models.
    self._mw = ensure_units(mw, "g/mol").magnitude
    self.heat_capacity_model.mw = self._mw
    self.eos_model.mw = self._mw

  def copy(self) -> 'Component':
    """Return a copy of the component."""
    return Component(
      self.id,
      self.name,
      self.phase,
      self.formula,
      self.mw,
      # Note that this data CAN be copied without problems.
      self.heat_capacity_model,
      self.eos_model,
    )

  @property
  def mw(self):
    """Molecular weight of the component (g/mol)"""
    return self._mw
  
  def cp_molar(self, T):
    """Heat capacity at constant pressure (J/(mol·K))"""
    return self.heat_capacity_model.cp_molar(T)
  
  def cv_molar(self, T):
    """Heat capacity at constant volume (J/(mol·K))"""
    return self.heat_capacity_model.cv_molar(T)
  
  def h_molar(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Enthalpy (J/mol) relative to reference temperature"""
    h_t = self.heat_capacity_model.enthalpy_temperature_change_molar(T, T_ref)
    h_p = self.eos_model.enthalpy_pressure_change_molar(T, P_ref, P)
    return h_t + h_p
  
  def h_mass(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Enthalpy (J/kg) relative to reference temperature"""
    return self.h_molar(T, P, T_ref, P_ref) / self.mw
  
  def s_molar(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Entropy (J/(mol·K)) at given T and P"""
    s_t = self.heat_capacity_model.entropy_temperature_change_molar(T, T_ref)
    s_p = self.eos_model.entropy_pressure_change_molar(T, P_ref, P)
    return s_t + s_p
  
  def s_mass(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Entropy (J/(kg·K)) at given T and P"""
    return self.s_molar(T, P, T_ref, P_ref) / self.mw
  
  def density_mass(self, T, P):
    """Density (kg/m³) at given T and P"""
    return self.eos_model.density_mass(T, P)
  
  def density_molar(self, T, P):
    """Molar density (mol/m³) at given T and P"""
    return self.eos_model.density_molar(T, P)
  
  def v_molar(self, T, P):
    """Molar volume (m³/mol) at given T and P"""
    rho_molar = self.density_molar(T, P)
    if rho_molar == 0:
      return 0
    return 1 / rho_molar
  
  def v_mass(self, T, P):
    """Mass volume (m³/kg) at given T and P"""
    rho_mass = self.density_mass(T, P)
    if rho_mass == 0:
      return 0
    return 1 / rho_mass
  
  def to_data(self) -> ComponentData:
    """Serialize the component to a data object."""
    return ComponentData(
      id=self.id,
      name=self.name,
      phase=self.phase,
      formula=self.formula,
      mw=self.mw
    )
  
  def serialize(self) -> dict:
    """Serialize the component to a dictionary."""
    return self.to_data().model_dump()