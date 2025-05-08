from dataclasses import dataclass

## usar na service, que faz o request das taxas
@dataclass
class Dates:
    DATE_FORMAT = "%d/%m/%Y"
    default_days_delay = 360
    yields_days_delay = 3
    inflation_days_delay = 390
