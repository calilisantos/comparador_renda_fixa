from dataclasses import dataclass


@dataclass
class Dates:
    DATE_FORMAT = "%d/%m/%Y"
    default_days_delay = 360
    fees_days_delay = 3
    inflation_days_delay = 390


@dataclass
class Request:
    bacen_endpoint = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{ratio_code}/dados?formato=json&dataInicial={request_date}"
    cdi_code = 12
    ipc_code = 7465
    ipca_code = 433
    igpm_code = 189
    selic_code = 432
    ratio_key = "valor"
    response_index = -1
    response_range = 12


@dataclass
class Operations:
    factor_base = 1
    percent_value = 100
    reduce_initial = 0
    round_value = 2

