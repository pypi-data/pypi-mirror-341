from pydantic import BaseModel, model_validator


class ThermoInterval(BaseModel):
  """Stores data for a temperature interval in a thermo model."""
  T_min: float
  T_max: float
  coeffs: list[float]

  @model_validator(mode="after")
  def check_temperature_ranges(cls, data: 'ThermoInterval'):
    if data.T_min >= data.T_max:
      raise ValueError("T_min must be less than T_max")
    return data