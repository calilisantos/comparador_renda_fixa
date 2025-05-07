from datetime import datetime, timedelta
from functools import reduce
import requests

today = datetime.today()
request_date_format = "%d/%m/%Y"
yesterday = today - timedelta(days=1)
endpoint = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{ratio_code}/dados?formato=json&dataInicial={request_date}"

last_year = today - timedelta(days=390)
fees_request_date = yesterday.strftime(request_date_format)
index_request_date = last_year.strftime(request_date_format)

cdi_code = 12 # 4391
selic_code = 432 # 11 diário
ipc_code = 7465
ipca_code = 433
igpm_code = 189

def fetch_data(ratio_code, request_date):
    #função para o request - OK; outra para tratar a resposta - Refatorar; outra para converter a taxa para ano - Criar?
    response = requests.get(endpoint.format(ratio_code=ratio_code, request_date=request_date))
    response.raise_for_status()
    return response.json()

def get_ratio(response,ratio_code):
    if ratio_code == selic_code:
        return float(response[-1].get("valor"))  # para selic (que é anual)
    elif ratio_code == cdi_code:
        value = float(response[-1].get("valor")) / 100
        return round((((1 + value) ** 252) -1) * 100, 2) # para CDI (que é diário)
    else:
        compound_value = reduce(
            lambda acc, curr: (((1 + (acc/100)) * (1 + (float(curr["valor"]) / 100)))-1)*100,
            response[-12:],
            0
        )
        return round(compound_value, 2) # para inflação que são acumulado mensal

cdi_fee = get_ratio(response=fetch_data(ratio_code=cdi_code, request_date=fees_request_date),ratio_code=cdi_code)
selic_fee = get_ratio(response=fetch_data(ratio_code=selic_code, request_date=fees_request_date),ratio_code=selic_code)
ipc_fee = get_ratio(response=fetch_data(ratio_code=ipc_code, request_date=index_request_date),ratio_code=ipc_code)
ipca_fee = get_ratio(response=fetch_data(ratio_code=ipca_code, request_date=index_request_date),ratio_code=ipca_code)
igpm_fee = get_ratio(response=fetch_data(ratio_code=igpm_code, request_date=index_request_date),ratio_code=igpm_code)

print(
f"""
cdi_fee: {cdi_fee}
# selic_fee: {selic_fee}
# ipc_fee: {ipc_fee}
# ipca_fee: {ipca_fee}
# igpm_fee: {igpm_fee}
"""
)
