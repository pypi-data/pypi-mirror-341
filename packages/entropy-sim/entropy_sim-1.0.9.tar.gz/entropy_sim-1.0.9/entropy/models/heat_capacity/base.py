from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound='HeatCapacityBaseModel')


class HeatCapacityBaseModel(ABC):
  """Base class for heat capacity models."""
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
  def cp_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant pressure (J/mol·K)."""
    raise NotImplementedError("Molar heat capacity at constant pressure calculation not implemented.")
  
  @abstractmethod
  def cp_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant pressure (J/kg·K)."""
    raise NotImplementedError("Specific heat capacity at constant pressure calculation not implemented.")

  @abstractmethod
  def cv_molar(self, T: float) -> float:
    """Returns the molar heat capacity at constant volume (J/mol·K)."""
    raise NotImplementedError("Molar heat capacity at constant volume calculation not implemented.")
  
  @abstractmethod
  def cv_mass(self, T: float) -> float:
    """Returns the specific heat capacity at constant volume (J/kg·K)."""
    raise NotImplementedError("Specific heat capacity at constant volume calculation not implemented.")
  
  @abstractmethod
  def enthalpy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar enthalpy change between temperatures T1 and T2 (J/mol)."""
    raise NotImplementedError("Molar enthalpy change calculation not implemented.")
  
  @abstractmethod
  def enthalpy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific enthalpy change between temperatures T1 and T2 (J/kg)."""
    raise NotImplementedError("Specific enthalpy change calculation not implemented.")
  
  @abstractmethod
  def entropy_temperature_change_molar(self, T1: float, T2: float) -> float:
    """Returns the molar entropy change between temperatures T1 and T2 (J/mol·K)."""
    raise NotImplementedError("Molar entropy change calculation not implemented.")
  
  @abstractmethod
  def entropy_temperature_change_mass(self, T1: float, T2: float) -> float:
    """Returns the specific entropy change between temperatures T1 and T2 (J/kg·K)."""
    raise NotImplementedError("Specific entropy change calculation not implemented.")

  @property
  @abstractmethod
  def mw(self) -> float:
    """Molecular weight (g/mol)"""
    raise NotImplementedError("Molecular weight calculation not implemented.")
  
  @mw.setter
  def mw(self, mw: float):
    """Set the molecular weight (g/mol)."""
    raise NotImplementedError("Molecular weight setter not implemented.")

  @property
  @abstractmethod
  def model_name(self) -> str:
    """Returns the name of the model."""
    raise NotImplementedError("Model name calculation not implemented.")
