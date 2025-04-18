from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound='EosBaseModel')


class EosBaseModel(ABC):
  """Base class for equation of state models."""
  def __init__(self) -> None:
    pass

  @abstractmethod
  def to_data(self) -> BaseModel:
    """Convert the model to a data payload."""
    raise NotImplementedError("Subclasses must implement the `to_data` method")
  
  @classmethod
  @abstractmethod
  def to_dict(self) -> dict[str, Any]:
    """Convert the model to a dictionary."""
    raise NotImplementedError("Subclasses must implement the `to_dict` method")

  @classmethod
  @abstractmethod
  def from_data(cls: Type[T], data: BaseModel | dict[str, Any]) -> T:
    """Construct this class from a data payload."""
    raise NotImplementedError("Subclasses must implement the `from_data` method")
  
  @abstractmethod
  def density_mass(self, T: float, P: float) -> float:
    """Returns the density of the material in kg/m³."""
    raise NotImplementedError("Density mass calculation not implemented.")
  
  @abstractmethod
  def density_molar(self, T: float, P: float) -> float:
    """Returns the density of the material in mol/m³."""
    raise NotImplementedError("Density molar calculation not implemented.")
  
  @abstractmethod
  def entropy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Returns the entropy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/mol·K)."""
    raise NotImplementedError("Entropy pressure change calculation not implemented.")
  
  @abstractmethod
  def entropy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Returns the entropy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/kg·K)."""
    raise NotImplementedError("Entropy pressure change calculation not implemented.")
  
  @abstractmethod
  def enthalpy_pressure_change_molar(self, T: float, P1: float, P2: float) -> float:
    """Returns the enthalpy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/mol)."""
    raise NotImplementedError("Enthalpy pressure change calculation not implemented.")
  
  @abstractmethod
  def enthalpy_pressure_change_mass(self, T: float, P1: float, P2: float) -> float:
    """Returns the enthalpy change of the material when the pressure changes from P1 to P2 at a given temperature T (J/kg)."""
    raise NotImplementedError("Enthalpy pressure change calculation not implemented.")
  
  @property
  @abstractmethod
  def model_name(self) -> str:
    """Returns the name of the model."""
    raise NotImplementedError("Model name calculation not implemented.")
  
  @property
  @abstractmethod
  def mw(self) -> float:
    """Returns the molecular weight of the material in g/mol."""
    raise NotImplementedError("Molecular weight calculation not implemented.")
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight of the material in g/mol."""
    raise NotImplementedError("Molecular weight setter not implemented.")
