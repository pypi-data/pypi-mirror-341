import pandas as pd
import requests
from brynq_sdk_functions import Functions as BrynQFunctions
from .schemas.hours import VariableHoursSchema, FixedHoursSchema, VariableHoursUploadSchema


class Hours:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get_types(self,
                  company_id: str) -> pd.DataFrame:
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/hourcodes")

        df = self.nmbrs.get_paginated_result(request)

        return df


class VariableHours:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            employee_id: str,
            created_from: str = None,
            period: int = None,
            year: int = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if period:
            params['period'] = period
        if year:
            params['year'] = year
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}employees/{employee_id}/variablehours",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))
        df['employee_id'] = employee_id  # Add employee_id for tracking

        # Validate data using the schema
        valid_hours, invalid_hours = BrynQFunctions.validate_data(df=df, schema=VariableHoursSchema, debug=True)

        return valid_hours, invalid_hours

    def create(self,
               employee_id: str,
               data: dict):
        """
        Create a variable hour component for an employee.
        
        Args:
            employee_id: The employee ID
            data: Dictionary containing variable hours data with these fields:
                - hourCode (int, required): Code of the hour component
                - hours (float, required): Amount of hours to register
                - comment (str, optional): Comment for the hour component
                - costCenterId (UUID str, optional): UUID of the cost center
                - costUnitId (UUID str, optional): UUID of the cost unit
                - periodDetails (dict, optional): Period details with:
                    - period (dict): Year and period number
                    - unprotectedMode (bool, optional): Set to True for past changes
                    
        Returns:
            Response from the API
        """
        # Validate data using Pydantic schema
        schema = VariableHoursUploadSchema(**data)
        
        # Use the model dict directly
        payload = schema.dict(exclude_none=True)
        
        resp = self.nmbrs.session.post(
            url=f"{self.nmbrs.base_url}employees/{employee_id}/variablehours",
            json=payload
        )

        return resp

    def update(self,
               employee_id: str,
               params: dict):
        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/variablehours",
                                      params=params)
        return resp

    def delete(self,
               employee_id: str,
               hourcomponent_id: str):
        resp = self.nmbrs.session.delete(url=f"{self.nmbrs.base_url}employees/{employee_id}/hours/{hourcomponent_id}")
        return resp


class FixedHours:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            company_id: str,
            created_from: str = None,
            employee_id: str = None,
            period: int = None,
            year: int = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if employee_id:
            params['employeeId'] = employee_id
        if period:
            params['period'] = period
        if year:
            params['year'] = year
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedhours",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))
        
        if employee_id:
            df['employee_id'] = employee_id  # Add employee_id for tracking if available
        
        # Validate data using the schema
        valid_hours, invalid_hours = BrynQFunctions.validate_data(df=df, schema=FixedHoursSchema, debug=True)

        return valid_hours, invalid_hours

    def create(self,
               employee_id: str,
               params: dict):
        # TODO: implement required and optional fields
        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedhours",
                                       params=params)
        return resp

    def update(self,
               employee_id: str,
               params: dict):
        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/fixedhours",
                                      params=params)
        return resp

    def delete(self,
               employee_id: str,
               hourcomponent_id: str):
        resp = self.nmbrs.session.delete(url=f"{self.nmbrs.base_url}employees/{employee_id}/hours/{hourcomponent_id}")
        return resp