import pandas as pd
import requests
from dateutil.utils import today
from requests import HTTPError

from brynq_sdk_functions import Functions
from .schemas.costcenter import CostcenterSchema, EmployeeCostcenterSchema
from .schemas.costunit import CostunitSchema


class EmployeeCostcenter:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            created_from: str = None,
            employee_id: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        costcenters = pd.DataFrame()
        for company in self.nmbrs.company_ids:
            costcenters = pd.concat([costcenters, self._get(company, created_from, employee_id)])

        valid_costcenters, invalid_costcenters = Functions.validate_data(df=costcenters, schema=EmployeeCostcenterSchema, debug=True)

        return valid_costcenters, invalid_costcenters

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
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/costcenters",
                                   params=params)
        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='employeeCostCenters',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def update(self,
               employee_id: str,
               data: dict):

        required_fields = ["year", "period", "costcenter_id", "costunit_id"]
        allowed_fields = {}
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "employeeId": employee_id,
            "employeeCostCenters": [
                {
                    "costCenterId": data["costcenter_id"],
                    "costUnitId": data["costunit_id"],
                    "percentage": 100
                }
            ],
            "period": {
                "year": today().year,
                "period": today().month
            }
        }

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/employeecostcenter",
                                      json=payload)
        return resp


class Costcenter:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        costcenters = pd.DataFrame()
        for company in self.nmbrs.company_ids:
            costcenters = pd.concat([costcenters, self._get(company)])

        valid_costcenters, invalid_costcenters = Functions.validate_data(df=costcenters, schema=CostcenterSchema, debug=True)

        return valid_costcenters, invalid_costcenters

    def _get(self,
            company_id: str):
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/costcenters")
        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))

        return df


class Costunit:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        costunits = pd.DataFrame()
        for company in self.nmbrs.company_ids:
            costunits = pd.concat([costunits, self._get(company)])

        valid_costunits, invalid_costunits = Functions.validate_data(df=costunits, schema=CostunitSchema, debug=True)

        return valid_costunits, invalid_costunits

    def _get(self,
            company_id: str):
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/costunits")

        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))

        return df