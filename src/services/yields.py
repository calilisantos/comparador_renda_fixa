from functools import reduce
from models.yields import DefaultValues, Operations
from models.request import Request
from services.request import RequestService


class YieldsService:
    @staticmethod
    def _get_ratio(response, ratio_code):
        if ratio_code == Request.selic_code:
            return float(response[Request.response_index].get(Request.ratio_key))
        elif ratio_code == Request.cdi_code:
            value = float(response[Request.response_index].get(Request.ratio_key)) / Operations.percent_value
            return round(
                (((Operations.factor_base + value) ** Operations.util_days) - Operations.factor_base) * Operations.percent_value
                , Operations.round_value
            )
        else:
            compound_value = reduce(
                lambda acc, curr: (
                    (
                        (Operations.factor_base + (acc/Operations.percent_value)) *
                        (Operations.factor_base + (float(curr[Request.ratio_key]) / Operations.percent_value))
                    ) - Operations.factor_base
                ) * Operations.percent_value,
                response[-Request.response_range:],
                Operations.reduce_initial
            )
            return round(compound_value, Operations.round_value)

    @classmethod
    def get_yield(cls, ratio_code, request_date):
        try:
            response = RequestService.fetch_data(
                endpoint=Request.bacen_endpoint,
                ratio_code=ratio_code,
                request_date=request_date
            )
            return cls._get_ratio(response, ratio_code)
        except Exception:
            return DefaultValues.map_default.get(ratio_code)
