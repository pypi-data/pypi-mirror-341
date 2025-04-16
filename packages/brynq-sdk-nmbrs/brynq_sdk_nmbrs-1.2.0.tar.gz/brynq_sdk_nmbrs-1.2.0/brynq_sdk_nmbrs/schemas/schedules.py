from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
import pandera as pa
from pandera import Bool, Int
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions
from pydantic import BaseModel, Field


class ScheduleSchema(pa.DataFrameModel):
    schedule_id: Series[String] = pa.Field(coerce=True)
    start_date: Series[datetime] = pa.Field(coerce=True)
    parttime_percentage: Series[Float] = pa.Field(coerce=True)
    week1_hours_monday: Series[Float] = pa.Field(coerce=True)
    week1_hours_tuesday: Series[Float] = pa.Field(coerce=True)
    week1_hours_wednesday: Series[Float] = pa.Field(coerce=True)
    week1_hours_thursday: Series[Float] = pa.Field(coerce=True)
    week1_hours_friday: Series[Float] = pa.Field(coerce=True)
    week1_hours_saturday: Series[Float] = pa.Field(coerce=True)
    week1_hours_sunday: Series[Float] = pa.Field(coerce=True)
    week2_hours_monday: Series[Float] = pa.Field(coerce=True)
    week2_hours_tuesday: Series[Float] = pa.Field(coerce=True)
    week2_hours_wednesday: Series[Float] = pa.Field(coerce=True)
    week2_hours_thursday: Series[Float] = pa.Field(coerce=True)
    week2_hours_friday: Series[Float] = pa.Field(coerce=True)
    week2_hours_saturday: Series[Float] = pa.Field(coerce=True)
    week2_hours_sunday: Series[Float] = pa.Field(coerce=True)
    created_at: Series[datetime] = pa.Field(coerce=True)


class ScheduleHours(BaseModel):
    """Schedule hours for each day of the week"""
    hoursMonday: float = Field(..., description="Monday hours")
    hoursTuesday: float = Field(..., description="Tuesday hours")
    hoursWednesday: float = Field(..., description="Wednesday hours")
    hoursThursday: float = Field(..., description="Thursday hours")
    hoursFriday: float = Field(..., description="Friday hours")
    hoursSaturday: float = Field(..., description="Saturday hours")
    hoursSunday: float = Field(..., description="Sunday hours")


class SchedulePostSchema(BaseModel):
    """
    Pydantic model for schedule post data
    """
    startDate: datetime = Field(..., description="Start date of the schedule")
    hoursPerWeek: Optional[float] = Field(None, description="Hours per week")
    week1: ScheduleHours = Field(..., description="Week 1 schedule hours")
    week2: ScheduleHours = Field(..., description="Week 2 schedule hours")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "startDate": "2021-01-01T09:29:18Z",
                "hoursPerWeek": 40,
                "week1": {
                    "hoursMonday": 8,
                    "hoursTuesday": 8,
                    "hoursWednesday": 8,
                    "hoursThursday": 8,
                    "hoursFriday": 2.5,
                    "hoursSaturday": 0,
                    "hoursSunday": 0
                },
                "week2": {
                    "hoursMonday": 8,
                    "hoursTuesday": 8,
                    "hoursWednesday": 8,
                    "hoursThursday": 8,
                    "hoursFriday": 2.5,
                    "hoursSaturday": 0,
                    "hoursSunday": 0
                }
            }
        }