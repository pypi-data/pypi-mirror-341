from pint import UnitRegistry
import numpy as np
from typing import Literal

ureg = UnitRegistry()
Q_ = ureg.Quantity


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
  if quantity is None:
    return {
      "value": None,
      "units": None,
    }
  if isinstance(quantity, Q_):
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
