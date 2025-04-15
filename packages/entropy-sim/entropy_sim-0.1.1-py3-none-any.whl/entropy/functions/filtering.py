from entropy.core.phase import Phase
from entropy.core.mixture import Mixture


def filter_by_phase(mixture: Mixture, phase: Phase) -> Mixture:
  """Filter a mixture to only include components of a specific phase.
  
  Args:
    mixture: The mixture to filter
    phase: The phase to filter for
    
  Returns:
    A new mixture containing only components of the specified phase
  """
  # Find components with the specified phase
  filtered_components = []
  filtered_fractions = []
  
  for i, component in enumerate(mixture.components):
    if component.phase == phase:
      filtered_components.append(component)
      filtered_fractions.append(mixture.mole_fractions[i])
  
  # If no components match the phase, return an empty mixture
  if not filtered_components:
    return Mixture([], [], basis="mole")
  
  # Create a new mixture with the filtered components
  filtered_mixture = Mixture(filtered_components, filtered_fractions, basis="mole")
  
  # Set the same temperature and pressure as the original mixture
  if mixture.T is not None:
    filtered_mixture.T = mixture.T
  if mixture.P is not None:
    filtered_mixture.P = mixture.P
    
  return filtered_mixture


def solids(mixture: Mixture) -> Mixture:
  """Extract only the solid components from a mixture.
  
  Returns:
    A new mixture containing only solid components
  """
  return filter_by_phase(mixture, Phase.SOLID)


def liquids(mixture: Mixture) -> Mixture:
  """Extract only the liquid components from a mixture.
  
  Returns:
    A new mixture containing only liquid components
  """
  return filter_by_phase(mixture, Phase.LIQUID)


def gases(mixture: Mixture) -> Mixture:
  """Extract only the gas components from a mixture.
  
  Returns:
    A new mixture containing only gas components
  """
  return filter_by_phase(mixture, Phase.GAS)


def aqueous(mixture: Mixture) -> Mixture:
  """Extract only the aqueous components from a mixture.
  
  Returns:
    A new mixture containing only aqueous components
  """
  return filter_by_phase(mixture, Phase.AQUEOUS)
