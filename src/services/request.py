import requests


class RequestService:
    @staticmethod
    def fetch_data(endpoint, ratio_code, request_date):
        response = requests.get(endpoint.format(ratio_code=ratio_code, request_date=request_date))
        response.raise_for_status()
        return response.json()
