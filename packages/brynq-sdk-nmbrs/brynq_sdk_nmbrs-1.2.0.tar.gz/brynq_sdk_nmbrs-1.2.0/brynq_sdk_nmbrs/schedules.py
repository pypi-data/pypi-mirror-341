import pandas as pd
import requests
import math
from brynq_sdk_functions import Functions
from .schemas.schedules import ScheduleSchema, SchedulePostSchema, ScheduleHours
from datetime import datetime
from typing import Dict, Any


class Schedule:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            created_from: str = None,
            employee_id: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        schedules = pd.DataFrame()
        for company in self.nmbrs.company_ids:
            schedules = pd.concat([schedules, self._get(company, created_from, employee_id)])

        valid_schedules, invalid_schedules = Functions.validate_data(df=schedules, schema=ScheduleSchema, debug=True)

        return valid_schedules, invalid_schedules

    def _get(self,
            company_id: str,
            created_from: str = None,
            employee_id: str = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if employee_id:
            params['employeeId'] = employee_id

        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/schedules",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='schedules',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def create(self,
               employee_id: str,
               data: dict):
        """
        Create a new schedule for an employee using Pydantic validation
        
        Args:
            employee_id: The employee ID
            data: Schedule data dictionary with the following keys:
                - start_date_schedule: Start date of the schedule
                - weekly_hours: Hours per week (optional)
                - hours_monday, hours_tuesday, etc.: Hours for each day
                
        Returns:
            Response from the API
        """
        # Transform data to match schema
        schedule_data = {}
        
        # Required field
        if "start_date_schedule" in data:
            schedule_data["startDate"] = data["start_date_schedule"]
        
        # Optional field
        if "weekly_hours" in data:
            # Handle NaN values
            if not isinstance(data["weekly_hours"], float) or not math.isnan(data["weekly_hours"]):
                schedule_data["hoursPerWeek"] = data["weekly_hours"]
        
        # Create week1 and week2 data
        week1_data = {}
        week2_data = {}
        
        day_mapping = {
            "hours_monday": "hoursMonday",
            "hours_tuesday": "hoursTuesday",
            "hours_wednesday": "hoursWednesday",
            "hours_thursday": "hoursThursday",
            "hours_friday": "hoursFriday",
            "hours_saturday": "hoursSaturday",
            "hours_sunday": "hoursSunday"
        }
        
        # Populate week1 data
        for day, api_day in day_mapping.items():
            if day in data and (not isinstance(data[day], float) or not math.isnan(data[day])):
                week1_data[api_day] = data[day]
            else:
                # Default to 0 hours if not specified
                week1_data[api_day] = 0.0
        
        # For now, set week2 same as week1 (can be adjusted if needed)
        week2_data = week1_data.copy()
        
        schedule_data["week1"] = week1_data
        schedule_data["week2"] = week2_data
        
        # Validate with Pydantic schema
        try:
            validated_data = SchedulePostSchema(**schedule_data)
            
            # Use the validated data for the API call
            resp = self.nmbrs.session.post(
                url=f"{self.nmbrs.base_url}employees/{employee_id}/schedule",
                json=validated_data.dict()
            )
            return resp
            
        except Exception as e:
            raise ValueError(f"Schedule validation failed: {str(e)}")
