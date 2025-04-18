from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound='SerializableMixin')


class SerializableMixin(ABC):
  """Abstract base class for serializable models.
  
  * `to_data`: Convert the model to a data payload (Pydantic model).
  * `to_dict`: Convert the model to a dictionary, useful for storing in a database.
  * `from_data`: Construct this class from a data payload.
  """
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
  