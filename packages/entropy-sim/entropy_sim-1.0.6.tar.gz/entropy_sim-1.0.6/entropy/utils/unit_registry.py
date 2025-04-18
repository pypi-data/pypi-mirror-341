import numpy as np
from typing import Literal
import pint

# Default registry (used if no external one is provided)
_default_ureg = pint.UnitRegistry()

# Current registry - starts with the default
_current_ureg = _default_ureg

Q_ = _current_ureg.Quantity


def set_registry(external_ureg: pint.UnitRegistry):
  """Set the unit registry to use throughout the library.
  
  IMPORTANT: Must be called before any other imports from this library.
  """
  global _current_ureg, Q_
  _current_ureg = external_ureg
  Q_ = _current_ureg.Quantity
    

def get_registry() -> pint.UnitRegistry:
  """Get the current unit registry used by the library."""
  return _current_ureg


def ensure_units(value: float | Q_, units: str) -> Q_:
  """Ensure a value is a Quantity with the specified units."""
  if isinstance(value, (float, int)):
    return Q_(value, units)
  elif isinstance(value, Q_):
    return value.to(units)
  else:
    raise ValueError(f"Invalid value: {value}")
    

def convert_numpy_to_python(value: Q_ | None) -> dict[str, str | float]:
  """Convert a numpy float to a python float."""
  if value is None:
    return None
  if isinstance(value, (np.float32, np.float64)):
    return float(value)
  if isinstance(value, (np.int32, np.int64)):
    return int(value)
  return value


def serialize_quantity(quantity: Q_ | float | int | None, units: Literal["short", "long"] = "short") -> dict[str, str | float]:
  """Serialize a `Quantity` object to a dictionary."""
  print("serialize_quantity", quantity, type(quantity))
  if quantity is None:
    return {
      "value": None,
      "units": None,
    }
  if isinstance(quantity, (Q_, pint.Quantity)):
    if units == "short":
      return {
        "value": convert_numpy_to_python(quantity.magnitude),
        "units": "{unit:~P}".format(unit=quantity.units),
      }
    else:
      return {
        "value": convert_numpy_to_python(quantity.magnitude),
        "units": str(quantity.units),
      }
  else:
    return {
      "value": convert_numpy_to_python(quantity),
      "units": None,
    }
