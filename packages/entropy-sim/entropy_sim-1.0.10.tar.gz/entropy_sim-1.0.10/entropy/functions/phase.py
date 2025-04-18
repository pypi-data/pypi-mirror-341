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
