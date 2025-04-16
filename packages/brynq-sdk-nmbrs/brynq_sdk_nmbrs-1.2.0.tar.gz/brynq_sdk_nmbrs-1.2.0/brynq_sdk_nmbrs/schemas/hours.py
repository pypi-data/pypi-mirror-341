import pandera as pa
from pandera.typing import Series, String, Float, DateTime
import pandas as pd
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from brynq_sdk_functions import BrynQPanderaDataFrameModel


class VariableHoursSchema(BrynQPanderaDataFrameModel):
    hour_component_id: Series[String] = pa.Field(coerce=True)  # UUID
    hour_code: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    hour_code_description: Series[String] = pa.Field(coerce=True, nullable=True)
    hours: Series[Float] = pa.Field(coerce=True)
    cost_center_id: Series[String] = pa.Field(coerce=True, nullable=True)  # UUID
    cost_unit_id: Series[String] = pa.Field(coerce=True, nullable=True)  # UUID
    comment: Series[String] = pa.Field(coerce=True, nullable=True)
    created_at: Series[DateTime] = pa.Field(coerce=True)
    employee_id: Series[String] = pa.Field(coerce=True)  # Added for tracking

    class Config:
        coerce = True

    class _Annotation:
        primary_key = "hour_component_id"
        foreign_keys = {
            "employee_id": {
                "parent_schema": "EmployeeSchema",
                "parent_column": "employee_id",
                "cardinality": "N:1"
                }
         }

class FixedHoursSchema(BrynQPanderaDataFrameModel):
    hour_component_id: Series[String] = pa.Field(coerce=True)
    hour_code: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    hour_code_description: Series[String] = pa.Field(nullable=True, coerce=True)
    hours: Series[Float] = pa.Field(coerce=True)
    cost_center_id: Series[String] = pa.Field(nullable=True, coerce=True)
    cost_unit_id: Series[String] = pa.Field(nullable=True, coerce=True)
    comment: Series[String] = pa.Field(nullable=True, coerce=True)
    end_year: Series[pd.Int64Dtype] = pa.Field(nullable=True, coerce=True)
    end_period: Series[pd.Int64Dtype] = pa.Field(nullable=True, coerce=True)
    created_at: Series[String] = pa.Field(coerce=True)
    employee_id: Series[String] = pa.Field(coerce=True, nullable=True)  # Added for tracking

    class Config:
        coerce = True

    class _Annotation:
        primary_key = "hour_component_id"
        foreign_keys = {
            "employee_id": {
                "parent_schema": "EmployeeSchema",
                "parent_column": "employee_id",
                "cardinality": "N:1"
                }
            }

# Pydantic schemas for API operations

class Period(BaseModel):
    """Period representation for Nmbrs API."""
    year: int
    period: int


class PeriodPost(BaseModel):
    """Period details for posting to Nmbrs API."""
    period: Period
    unprotectedMode: Optional[bool] = Field(default=None, description="Unprotected Mode needs to be set to true when making changes in the past. Default is false.")


class VariableHoursUploadSchema(BaseModel):
    """Schema for uploading variable hours to Nmbrs API."""
    hourCode: int = Field(..., description="Code of the hour component")
    hours: float = Field(..., description="Amount of hours to be registered on this hour component")
    comment: Optional[str] = Field(default=None, description="Comment of the hour component")
    costCenterId: Optional[UUID] = Field(default=None, description="UUID of the cost center")
    costUnitId: Optional[UUID] = Field(default=None, description="UUID of the cost unit")
    periodDetails: Optional[PeriodPost] = Field(
        default=None,
        description="If no period is specified, it will be added to the current period."
    )

    class Config:
        """Configuration for the schema."""
        allow_population_by_field_name = True
