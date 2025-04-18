from entropy.core.component import Component, ComponentData
from entropy.core.phase import Phase
from entropy.models.eos.base import EosBaseModel
from entropy.models.heat_capacity.base import HeatCapacityBaseModel
from entropy.utils.constants import Constants
from entropy.utils.unit_registry import Q_, ensure_units


class MultiphaseComponent(Component):
  """A component that can exist in multiple phases.
  
  This class is actually a wrapper around several `Component` objects,
  each of which is a different phase that the component can exist in.

  It has the same interface as a `Component`.

  At any given time, only one of the `Component` objects will be active.
  """
  def __init__(
    self,
    id: str,
    name: str,
    phase: Phase,
    formula: dict[str, int | float],
    mw: Q_ | float,
    subcomponents: dict[Phase, Component]
  ):
    """Initialize a multiphase component.
    
    Args:
    * `id`: Unique identifier for the component
    * `name`: Name of the component
    * `phase`: The active phase of the component
    * `formula`: Chemical formula of the component
    * `subcomponents`: Mapping of phases to `Component` objects
    """
    self._id = id
    self._name = name
    self._phase = phase
    self._formula = formula
    self._subcomponents = subcomponents
    self._mw = ensure_units(mw, "g/mol").magnitude

    # Validate that the subcomponents are valid
    for phase, component in subcomponents.items():
      if component.id != id:
        raise ValueError(f"Subcomponent for phase '{phase}' has a different ID than the multiphase component.")
      if component.name != name:
        raise ValueError(f"Subcomponent for phase '{phase}' has a different name than the multiphase component.")
      if component.formula != formula:
        raise ValueError(f"Subcomponent for phase '{phase}' has a different formula than the multiphase component.")

  @property
  def id(self) -> str:
    """The ID of the component."""
    return self._id
  
  @property
  def name(self) -> str:
    """The name of the component."""
    return self._name
  
  @property
  def formula(self) -> dict[str, int | float]:
    """The formula of the component."""
    return self._formula

  @property
  def phase(self) -> Phase:
    """The active phase of the component."""
    return self._phase
  
  @phase.setter
  def phase(self, phase: Phase):
    """Set the active phase of the component."""
    if phase not in self._subcomponents:
      raise ValueError(f"Cannot set phase '{phase}' for '{self._name}' because it is not supported.")
    self._phase = phase

  def change_phase(self, phase: Phase):
    """An alias for `phase.setter`."""
    self.phase = phase
  
  @property
  def supported_phases(self) -> list[Phase]:
    """The phases that the component can exist in."""
    return list(self._subcomponents.keys())

  @property
  def subcomponents(self) -> dict[Phase, Component]:
    """The subcomponents of the component."""
    return self._subcomponents
  
  @property
  def active_subcomponent(self) -> Component:
    """The active subcomponent of the component."""
    return self._subcomponents[self._phase]
  
  @property
  def mw(self):
    """Molecular weight of the component (g/mol)"""
    return self.active_subcomponent.mw
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight of the component (g/mol)."""
    self._mw = mw
  
  def cp_molar(self, T):
    """Heat capacity at constant pressure (J/(mol·K))"""
    return self.active_subcomponent.cp_molar(T)
  
  def cv_molar(self, T):
    """Heat capacity at constant volume (J/(mol·K))"""
    return self.active_subcomponent.cv_molar(T)
  
  def h_molar(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Enthalpy (J/mol) relative to reference temperature"""
    return self.active_subcomponent.h_molar(T, P, T_ref, P_ref)
  
  def h_mass(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Enthalpy (J/kg) relative to reference temperature"""
    return self.active_subcomponent.h_molar(T, P, T_ref, P_ref) / self.mw
  
  def s_molar(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Entropy (J/(mol·K)) at given T and P"""
    return self.active_subcomponent.s_molar(T, P, T_ref, P_ref)
  
  def s_mass(self, T, P, T_ref=Constants.DEFAULT_T_REF, P_ref=Constants.DEFAULT_P_REF):
    """Entropy (J/(kg·K)) at given T and P"""
    return self.active_subcomponent.s_mass(T, P, T_ref, P_ref)
  
  def density_mass(self, T, P):
    """Density (kg/m³) at given T and P"""
    return self.active_subcomponent.density_mass(T, P)
  
  def density_molar(self, T, P):
    """Molar density (mol/m³) at given T and P"""
    return self.active_subcomponent.density_molar(T, P)
  
  def v_molar(self, T, P):
    """Molar volume (m³/mol) at given T and P"""
    return self.active_subcomponent.v_molar(T, P)
  
  def v_mass(self, T, P):
    """Mass volume (m³/kg) at given T and P"""
    return self.active_subcomponent.v_mass(T, P)
  
  @property
  def heat_capacity_model(self) -> HeatCapacityBaseModel:
    """The heat capacity model of the component."""
    return self.active_subcomponent.heat_capacity_model

  @property
  def eos_model(self) -> EosBaseModel:
    """The equation of state model of the component."""
    return self.active_subcomponent.eos_model
  
  def copy(self) -> 'MultiphaseComponent':
    """Return a copy of the component."""
    return MultiphaseComponent(
      id=self.id,
      name=self.name,
      phase=self.phase,
      formula=self.formula,
      mw=self.mw,
      subcomponents={phase: component.copy() for phase, component in self.subcomponents.items()},
    )

  def to_data(self) -> ComponentData:
    """Serialize the component to a data object."""
    return self.active_subcomponent.to_data()
  
  def serialize(self) -> dict:
    """Serialize the component to a dictionary."""
    return self.active_subcomponent.serialize()
