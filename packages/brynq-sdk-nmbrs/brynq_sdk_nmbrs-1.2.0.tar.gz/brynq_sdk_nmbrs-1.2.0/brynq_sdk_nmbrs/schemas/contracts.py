import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions
from brynq_sdk_functions import BrynQPanderaDataFrameModel


class ContractSchema(BrynQPanderaDataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    contract_id: Series[String] = pa.Field(coerce=True)
    start_date: Series[DateTime] = pa.Field(coerce=True)
    trial_period: Series[String] = pa.Field(coerce=True, nullable=True)
    end_date: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    indefinite: Series[Bool] = pa.Field(coerce=True)
    written_contract: Series[Bool] = pa.Field(coerce=True)
    hours_per_week: Series[Float] = pa.Field(coerce=True, nullable=True)
    created_at: Series[DateTime] = pa.Field(coerce=True)
    # company_id: Series[String] = pa.Field(coerce=True)

    class _Annotation:
        primary_key = "contract_id"
        foreign_keys = {
            "employee_id": {
                "parent_schema": "EmployeeSchema",
                "parent_column": "employee_id",
                "cardinality": "N:1"
            }
        }