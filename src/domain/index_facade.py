from configs.components import Text
from configs.inflation import InflationTypes
from models.request import Request
from models.yields import DefaultValues
from services.date import DateService
from services.index import IndexService


class IndexFacade:
    def __init__(self, current_date):
        self.date_service = DateService(current_date=current_date)
        self.yields_request_date = self.date_service.set_yields_request_date()
        self.index_request_date = self.date_service.set_index_request_date()

    def get_all_yields(self):
        return {
            Text.cdi_label: IndexService.get_yield(Request.cdi_code, self.yields_request_date),
            Text.selic_label: IndexService.get_yield(Request.selic_code, self.yields_request_date),
            Text.poupanca_label: DefaultValues.POUPANCA_YIELD,
            InflationTypes.IPC: IndexService.get_yield(Request.ipc_code, self.index_request_date),
            InflationTypes.IPCA: IndexService.get_yield(Request.ipca_code, self.index_request_date),
            InflationTypes.IGPM: IndexService.get_yield(Request.igpm_code, self.index_request_date)
        }
