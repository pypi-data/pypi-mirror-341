from entropy.core.phase import Phase
from entropy.core.multiphase_component import MultiphaseComponent
from entropy.core.mixture import Mixture


def phase_transition(mixture: Mixture, from_phase: Phase, to_phase: Phase, skip_incompatible: bool = True) -> Mixture:
  """Perform a phase transition on a mixture.
  
  - If `skip_incompatible` is `True`, then components that do not support the new phase will be skipped.
  - Otherwise, an error will be raised.
  """
  out = mixture.copy()
  for component in out.components:
    if component.phase == from_phase:
      if not isinstance(component, MultiphaseComponent):
        continue
      if skip_incompatible and to_phase not in component.supported_phases:
        continue
      component.change_phase(to_phase)

  # Update the temperature and pressure of the new mixture (same as before).
  out.T = mixture.T
  out.P = mixture.P

  return out


def dissolve(mixture: Mixture) -> Mixture:
  """Perform a solid -> aqueous phase transition."""
  return phase_transition(mixture, Phase.SOLID, Phase.AQUEOUS)


def precipitate(mixture: Mixture) -> Mixture:
  """Perform an aqueous -> solid phase transition."""
  return phase_transition(mixture, Phase.AQUEOUS, Phase.SOLID)


def evaporate(mixture: Mixture) -> Mixture:
  """Perform a liquid -> gas phase transition."""
  return phase_transition(mixture, Phase.LIQUID, Phase.GAS)


def condense(mixture: Mixture) -> Mixture:
  """Perform a gas -> liquid phase transition."""
  return phase_transition(mixture, Phase.GAS, Phase.LIQUID)


def melt(mixture: Mixture) -> Mixture:
  """Perform a solid -> liquid phase transition."""
  return phase_transition(mixture, Phase.SOLID, Phase.LIQUID)


def freeze(mixture: Mixture) -> Mixture:
  """Perform a liquid -> solid phase transition."""
  return phase_transition(mixture, Phase.LIQUID, Phase.SOLID)


def sublimate(mixture: Mixture) -> Mixture:
  """Perform a solid -> gas phase transition."""
  return phase_transition(mixture, Phase.SOLID, Phase.GAS)


def deposit(mixture: Mixture) -> Mixture:
  """Perform a gas -> solid phase transition."""
  return phase_transition(mixture, Phase.GAS, Phase.SOLID)


# from typing import Literal

# from scaler_lang.mixtures.mixture_base import Phase
# from scaler_lang.mixtures.mixture_wrapper import MixtureWrapper
# from scaler_lang.objects.mass_flow import MassFlowObject
# from scaler_lang.models.parameter import MaterialValue


# def filter_component_asset_ids(flow: MassFlowObject, component_asset_ids: list[str]) -> MassFlowObject:
#   """Return a new mass flow object with only the specified component IDs."""
#   mixture = flow.mixture

#   indices = [i for i, id in enumerate(mixture.ids) if id in component_asset_ids]
#   ids = [mixture.ids[i] for i in indices]
#   names = [mixture.names[i] for i in indices]
#   phases = [mixture.phases[i] for i in indices]

#   fractions = [mixture.fractions[i] for i in indices]
#   total_fraction = sum(fractions)

#   # Get the dominant phase by fraction.
#   phase_fractions = {}
#   for i, phase in enumerate(phases):
#     if phase not in phase_fractions:
#       phase_fractions[phase] = 0
#     phase_fractions[phase] += fractions[i]

#   if len(phase_fractions) == 0:
#     dominant_phase: str = "liquid"
#   else:
#     dominant_phase: str = max(phase_fractions, key=phase_fractions.get)

#   # Determine the minor components - anything that is not the dominant phase.
#   minor = [phase != dominant_phase for phase in phases]

#   new_flow = MassFlowObject()

#   # Set the rate of the new flow, which will be some fraction of the original flow.
#   if mixture.by == "mass":
#     new_flow.rate.m = flow.rate.m * total_fraction
#   elif mixture.by == "mole":
#     new_flow.rate.x = flow.rate.x * total_fraction
#   else:
#     raise NotImplementedError(f"Unsupported 'by' value '{mixture.by}'.")

#   new_flow.mixture = MixtureWrapper(
#     ids=ids,
#     names=names,
#     phases=phases,
#     minor=minor,
#     fractions=fractions,
#     by=mixture.by,
#     materials=mixture.materials,
#   )

#   # Determine the filtered flow. This is required in order for equations like:
#   # `OutputFlow = 0.1 * solids(InputFlow)` to work.
#   mw = new_flow.mixture.mw
#   if mw is None or mw == 0:
#     new_flow.rate.mw = 1
#   else:
#     new_flow.rate.mw = mw
#   new_flow.rate.rho_mass = new_flow.mixture.rho_mass
#   new_flow.mixture.T = flow.mixture.T
#   new_flow.mixture.P = flow.mixture.P

#   # Copy the cycle properties from the original flow.
#   new_flow.upstream = flow.upstream
#   new_flow.downstream = flow.downstream

#   new_flow.determine()

#   return new_flow


# def filter_phase(
#   flow: MassFlowObject,
#   filter_phase: Phase,
#   behavior: Literal["include", "exclude"] = "include"
# ) -> MassFlowObject:
#   """Return a new mass flow object, filtered by phase of matter."""
#   if behavior not in ["include", "exclude"]:
#     raise ValueError(f"Invalid filtering behavior '{behavior}'. Must be either 'include' or 'exclude'.")

#   if behavior == "include":
#     component_asset_ids = [
#       id for i, id in enumerate(flow.mixture.ids) if flow.mixture.phases[i] == filter_phase
#     ]
#   else:
#     component_asset_ids = [
#       id for i, id in enumerate(flow.mixture.ids) if flow.mixture.phases[i] != filter_phase
#     ]

#   return filter_component_asset_ids(flow, component_asset_ids)


# def phase_transition(flow: MassFlowObject, from_phase: Phase, to_phase: Phase) -> MassFlowObject:
#   """Return a new mass flow object, where phases have been converted to the new phase."""
#   if from_phase == to_phase:
#     print("Warning: Phase transition from and to the same phase. Returning original flow.")
#     return flow

#   updated_phases = []
#   for i, phase in enumerate(flow.mixture.phases):
#     if phase == from_phase:
#       updated_phases.append(to_phase)
#     else:
#       updated_phases.append(phase)

#   new_flow = MassFlowObject()

#   if flow.mixture.by == "mass":
#     new_flow.rate.m = flow.rate.m
#   elif flow.mixture.by == "mole":
#     new_flow.rate.x = flow.rate.x
#   else:
#     raise NotImplementedError(f"Unsupported 'by' value '{flow.mixture.by}'.")

#   # Create a new mixture with the new phase.
#   new_flow.mixture = MixtureWrapper(
#     ids=flow.mixture.ids,
#     names=flow.mixture.names,
#     phases=updated_phases,
#     minor=flow.mixture.minor,
#     fractions=flow.mixture.fractions,
#     by=flow.mixture.by,
#     materials=flow.mixture.materials,
#   )

#   # Determine the filtered flow.
#   mw = new_flow.mixture.mw
#   if mw is None or mw == 0:
#     new_flow.rate.mw = 1
#   else:
#     new_flow.rate.mw = mw
#   new_flow.rate.rho_mass = new_flow.mixture.rho_mass
#   new_flow.mixture.T = flow.mixture.T
#   new_flow.mixture.P = flow.mixture.P

#   # Copy the cycle properties from the original flow.
#   new_flow.upstream = flow.upstream
#   new_flow.downstream = flow.downstream

#   new_flow.determine()

#   return new_flow


# def filter_solids(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by solid phase."""
#   return filter_phase(flow, "solid", behavior="include")


# def filter_liquids(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by liquid phase."""
#   return filter_phase(flow, "liquid", behavior="include")


# def filter_gases(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by gas phase."""
#   return filter_phase(flow, "gas", behavior="include")


# def filter_aqueous(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by aqueous phase."""
#   return filter_phase(flow, "aqueous", behavior="include")


# def filter_nonsolids(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by non-solid phase."""
#   return filter_phase(flow, "solid", behavior="exclude")


# def filter_nonliquids(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by non-liquid phase."""
#   return filter_phase(flow, "liquid", behavior="exclude")


# def filter_nongases(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by non-gas phase."""
#   return filter_phase(flow, "gas", behavior="exclude")


# def filter_nonaqueous(flow: MassFlowObject) -> MassFlowObject:
#   """Return a new mass flow object, filtered by non-aqueous phase."""
#   return filter_phase(flow, "aqueous", behavior="exclude")


# def include_components(flow: MassFlowObject, components: str | list[str] | MaterialValue | list[MaterialValue]) -> MassFlowObject:
#   """Return a new mass flow object, filtered by component ID."""
#   if not isinstance(components, list):
#     components = [components]
#   component_asset_ids = list(map(lambda x: x.assetId if isinstance(x, MaterialValue) else x, components))
#   return filter_component_asset_ids(flow, component_asset_ids)


# def exclude_components(flow: MassFlowObject, components: str | list[str] | MaterialValue | list[MaterialValue]) -> MassFlowObject:
#   """Return a new mass flow object, excluding the specified component IDs."""
#   if not isinstance(components, list):
#     components = [components]
#   component_asset_ids = list(map(lambda x: x.assetId if isinstance(x, MaterialValue) else x, components))
#   included_ids = [id for id in flow.mixture.ids if id not in component_asset_ids]
#   return filter_component_asset_ids(flow, included_ids)


# def dissolve(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a solid -> aqueous phase transition."""
#   return phase_transition(flow, "solid", "aqueous")


# def precipitate(flow: MassFlowObject) -> MassFlowObject:
#   """Perform an aqueous -> solid phase transition."""
#   return phase_transition(flow, "aqueous", "solid")


# def evaporate(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a liquid -> gas phase transition."""
#   return phase_transition(flow, "liquid", "gas")


# def condense(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a gas -> liquid phase transition."""
#   return phase_transition(flow, "gas", "liquid")


# def melt(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a solid -> liquid phase transition."""
#   return phase_transition(flow, "solid", "liquid")


# def freeze(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a liquid -> solid phase transition."""
#   return phase_transition(flow, "liquid", "solid")


# def sublimate(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a solid -> gas phase transition."""
#   return phase_transition(flow, "solid", "gas")


# def deposit(flow: MassFlowObject) -> MassFlowObject:
#   """Perform a gas -> solid phase transition."""
#   return phase_transition(flow, "gas", "solid")
