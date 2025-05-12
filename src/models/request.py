class Request:
    bacen_endpoint = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{ratio_code}/dados?formato=json&dataInicial={request_date}"
    cache_interval = 60 ** 3 # one hour
    cdi_code = 12
    ipc_code = 7465
    ipca_code = 433
    igpm_code = 189
    selic_code = 432
    ratio_key = "valor"
    response_index = -1
    response_range = 12
