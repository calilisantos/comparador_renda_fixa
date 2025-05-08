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
    util_days = 252


@dataclass
class DefaultValues:
    CDI_FEE = 14.39
    SELIC_FEE = 14.5
    IPC_FEE = 4.0
    IPCA_FEE = 6.5
    IGPM_FEE = 5.0
    POUPANCA_FEE = 6.17
    INDEX_TYPE = 'IPCA'


@dataclass
class Tax:
    anual_fee = 0.2
    anual_range = 360
    beyond_fee = 0.15
    bianual_fee = 0.175
    bianual_range = 720
    free_tax = 0
    semester_fee = 0.225
    semester_range = 180

