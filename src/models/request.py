from models.yields import DefaultValues


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

class DefaultValues:
    map_default = {
        Request.cdi_code: DefaultValues.CDI_YIELD,
        Request.ipc_code: DefaultValues.IPC_YIELD,
        Request.ipca_code: DefaultValues.IPCA_YIELD,
        Request.igpm_code: DefaultValues.IGPM_YIELD,
        Request.selic_code: DefaultValues.SELIC_YIELD
    }
