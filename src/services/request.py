import requests
import streamlit as st
from models.request import Request


class RequestService:
    @staticmethod
    @st.cache_data(ttl=Request.cache_interval)
    def fetch_data(endpoint, ratio_code, request_date):
        response = requests.get(endpoint.format(ratio_code=ratio_code, request_date=request_date))
        response.raise_for_status()
        return response.json()
