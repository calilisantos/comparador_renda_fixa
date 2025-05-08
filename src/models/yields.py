from dataclasses import dataclass


@dataclass
class DefaultValues:
    CDI_YIELD = 14.39
    SELIC_YIELD = 14.5
    IPC_YIELD = 4.0
    IPCA_YIELD = 6.5
    IGPM_YIELD = 5.0
    POUPANCA_YIELD = 6.17
    INDEX_TYPE = 'IPCA'


@dataclass
class Operations:
    factor_base = 1
    percent_value = 100
    reduce_initial = 0
    round_value = 2
    util_days = 252


@dataclass
class Tax:
    anual_yield = 0.2
    anual_range = 360
    beyond_yield = 0.15
    bianual_yield = 0.175
    bianual_range = 720
    free_tax = 0
    semester_yield = 0.225
    semester_range = 180

