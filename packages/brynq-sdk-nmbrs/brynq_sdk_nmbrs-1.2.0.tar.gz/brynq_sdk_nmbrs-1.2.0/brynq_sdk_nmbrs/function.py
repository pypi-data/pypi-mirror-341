import pandas as pd
import requests
from .schemas.function import FunctionSchema
from brynq_sdk_functions import Functions as BrynQFunctions


class EmployeeFunction:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            created_from: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        functions = pd.DataFrame()
        for company in self.nmbrs.company_ids:
            functions = pd.concat([functions, self._get(company, created_from)])

        valid_functions, invalid_functions = BrynQFunctions.validate_data(df=functions, schema=FunctionSchema, debug=True)

        return valid_functions, invalid_functions

    def _get(self,
            company_id: str,
            created_from: str = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        try:
            request = requests.Request(method='GET',
                                       url=f"{self.nmbrs.base_url}companies/{company_id}/employees/functions",
                                       params=params)

            data = self.nmbrs.get_paginated_result(request)
            df = pd.json_normalize(
                data,
                record_path='functions',
                meta=['employeeId']
            )
            df = self.nmbrs._rename_camel_columns_to_snake_case(df)
        except requests.HTTPError as e:
            df = pd.DataFrame()

        return df

    def update(self,
               employee_id: str,
               data: dict):

        required_fields = ["year", "period", "function_id"]
        allowed_fields = {}
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "functionId": data["function_id"],
            "periodDetails": {
                "year": data["year"],
                "period": data["period"]
            }
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/function",
                                      json=payload)
        return resp


class Functions:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self, debtor_id: str) -> pd.DataFrame:
        try:
            request = requests.Request(method='GET',
                                       url=f"{self.nmbrs.base_url}debtors/{debtor_id}/functions")

            data = self.nmbrs.get_paginated_result(request)
            df = pd.DataFrame(data)
            df = self.nmbrs._rename_camel_columns_to_snake_case(df)
        except requests.HTTPError as e:
            df = pd.DataFrame()

        return df