import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions


class EmployeeCostcenterSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    employee_cost_center_id: Series[String] = pa.Field(coerce=True)
    cost_centers_cost_center_id: Series[String] = pa.Field(coerce=True)
    cost_centers_code: Series[String] = pa.Field(coerce=True)
    cost_centers_description: Series[String] = pa.Field(coerce=True)
    cost_units_cost_unit_id: Series[String] = pa.Field(coerce=True)
    cost_units_code: Series[String] = pa.Field(coerce=True)
    cost_units_description: Series[String] = pa.Field(coerce=True)
    percentage: Series[Float] = pa.Field(coerce=True)
    default: Series[Bool] = pa.Field(coerce=True)
    period_year: Series[int] = pa.Field(coerce=True)
    period_period: Series[int] = pa.Field(coerce=True)
    created_at: Series[DateTime] = pa.Field(coerce=True)

class CostcenterSchema(pa.DataFrameModel):
    cost_center_id: Series[String] = pa.Field(coerce=True)
    code: Series[String] = pa.Field(coerce=True)
    description: Series[String] = pa.Field(coerce=True)