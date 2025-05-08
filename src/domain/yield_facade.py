from models.request import Request
from models.yields import DefaultValues
from services.date import DateService
from services.yields import YieldsService


class YieldFacade:
    def __init__(self, current_date):
        self.date_service = DateService(current_date=current_date)
        self.yields_request_date = self.date_service.set_yields_request_date()
        self.index_request_date = self.date_service.set_index_request_date()

    def get_all_yields(self):
        return {
            "cdi": YieldsService.get_yield(Request.cdi_code, self.yields_request_date),
            "selic": YieldsService.get_yield(Request.selic_code, self.yields_request_date),
            "ipc": YieldsService.get_yield(Request.ipc_code, self.index_request_date),
            "ipca": YieldsService.get_yield(Request.ipca_code, self.index_request_date),
            "igpm": YieldsService.get_yield(Request.igpm_code, self.index_request_date),
            "poupanca": DefaultValues.POUPANCA_YIELD
        }
