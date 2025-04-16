import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions


class CostunitSchema(pa.DataFrameModel):
    cost_unit_id: Series[String] = pa.Field(coerce=True)
    code: Series[String] = pa.Field(coerce=True)
    description: Series[String] = pa.Field(coerce=True)
