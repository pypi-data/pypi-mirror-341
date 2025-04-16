import math
import pandas as pd
import requests
from dateutil.utils import today

from .schemas.department import DepartmentSchema
from brynq_sdk_functions import Functions


class EmployeeDepartment:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            created_from: str = None,
            employee_id: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        departments = pd.DataFrame()
        for company in self.nmbrs.company_ids:
            departments = pd.concat([departments, self._get(company, created_from, employee_id)])

        valid_departments, invalid_departments = Functions.validate_data(df=departments, schema=DepartmentSchema, debug=True)

        return valid_departments, invalid_departments

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
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/departments",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='departments',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def update(self,
               employee_id: str,
               data: dict):

        required_fields = ["year", "period", "department_id"]
        allowed_fields = {}
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "departmentId": data["department_id"],
            "periodDetails": {
                "year": data["year"],
                "period": data["period"]
            }
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/department",
                                      json=payload)
        return resp


class Departments:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            debtor_id: str) -> pd.DataFrame:
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}debtors/{debtor_id}/departments")

        data = self.nmbrs.get_paginated_result(request)
        df = pd.DataFrame(data)
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df
