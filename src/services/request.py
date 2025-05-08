from functools import reduce
from models.date import Date
from models.yields import DefaultValues, Operations
from models.request import Request
import requests


# today = datetime.now() # deixar na main ou controller. É usada no request e no deal com data de vencimento
# def transform_date(days_diff, date_format=None): # mover para service do request
#     if date_format:
#         past_day = today - timedelta(days=days_diff)
#         return past_day.strftime(date_format)
#     return today + timedelta(days=days_diff)

default_date = date_svc.transform_date(days_diff=Date.default_days_delay) # mover para service do request

## Lógica do request -> mover para service

request_date_format = Date.DATE_FORMAT
yields_request_date = date_svc.transform_date(days_diff=Date.yields_days_delay, date_format=request_date_format)
index_request_date = date_svc.transform_date(days_diff=Date.inflation_days_delay, date_format=request_date_format)


def fetch_data(ratio_code, request_date):
    #função para o request - OK; outra para tratar a resposta - Refatorar; outra para converter a taxa para ano - Criar?
    response = requests.get(Request.bacen_endpoint.format(ratio_code=ratio_code, request_date=request_date))
    response.raise_for_status()
    return response.json()

def get_ratio(response,ratio_code):
    if ratio_code == Request.selic_code:
        return float(response[Request.response_index].get(Request.ratio_key))  # para selic (que é anual)
    elif ratio_code == Request.cdi_code:
        value = float(response[Request.response_index].get(Request.ratio_key)) / Operations.percent_value
        return round((((Operations.factor_base + value) ** Operations.util_days) -Operations.factor_base) * Operations.percent_value, Operations.round_value)
    else:
        compound_value = reduce(
            lambda acc, curr: (((Operations.factor_base + (acc/Operations.percent_value)) * (Operations.factor_base + (float(curr[Request.ratio_key]) / Operations.percent_value)))-Operations.factor_base)*Operations.percent_value,
            response[-Request.response_range:],
            Operations.reduce_initial
        )
        return round(compound_value, Operations.round_value) # para inflação que são acumulado mensal

try:
    cdi_yield = get_ratio(response=fetch_data(ratio_code=Request.cdi_code, request_date=yields_request_date),ratio_code=Request.cdi_code)
    selic_yield = get_ratio(response=fetch_data(ratio_code=Request.selic_code, request_date=yields_request_date),ratio_code=Request.selic_code)
    ipc_yield = get_ratio(response=fetch_data(ratio_code=Request.ipc_code, request_date=index_request_date),ratio_code=Request.ipc_code)
    ipca_yield = get_ratio(response=fetch_data(ratio_code=Request.ipca_code, request_date=index_request_date),ratio_code=Request.ipca_code)
    igpm_yield = get_ratio(response=fetch_data(ratio_code=Request.igpm_code, request_date=index_request_date),ratio_code=Request.igpm_code)
except:
    cdi_yield = DefaultValues.CDI_YIELD
    selic_yield = DefaultValues.SELIC_YIELD
    ipc_yield = DefaultValues.IPC_YIELD
    ipca_yield = DefaultValues.IPCA_YIELD
    igpm_yield = DefaultValues.IGPM_YIELD


poupanca_yield = DefaultValues.POUPANCA_YIELD
yield_input = poupanca_yield
index_yield = ipca_yield
index_type = DefaultValues.INDEX_TYPE