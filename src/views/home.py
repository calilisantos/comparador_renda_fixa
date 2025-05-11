from configs.components import Menu, Settings, Text
from models.yields import Operations
import streamlit as st


class HomeView:
    @staticmethod
    def show_main_title():
        return st.write(
            Text.main_title,
            unsafe_allow_html=Settings.ALLOW_HTML
        )

    @staticmethod
    def show_products_box():
        return st.selectbox(
            label=Text.product_label,
            options=Menu.product_options
        )

    @staticmethod
    def show_result_title():
        return st.write(
            Text.result_title,
            unsafe_allow_html=Settings.ALLOW_HTML
        )

    @staticmethod
    def show_metric(column, delta, label, value):
        return column.metric(
            border=Settings.METRIC_BORDER,
            delta=delta,
            label=label,
            value=value
        )
    
    @staticmethod
    def show_bond_type_radio():
        return st.radio(
            label=Text.yield_title,
            options=Menu.yield_options
        )

    @staticmethod
    def show_index_type_radio():
        return st.radio(
            label=Text.inflation_index_label,
            options=Menu.inflation_index_options
        )
    
    @staticmethod
    def show_maturity_type_radio():
        return st.radio(
            label=Text.maturity_label,
            options=Menu.maturity_options
        )
    
    @staticmethod
    def show_maturity_date_input(default_date):
        return st.date_input(
            label=Text.date_label,
            format=Text.date_input_format,
            value=default_date
        )

    @staticmethod
    def show_maturity_in_days_input():
        return st.number_input(
            label=Text.days_maturity_label,
            min_value=Operations.factor_base
        )

    @staticmethod
    def show_hold_until_maturity_radio(key):
        return st.radio(
            label=Text.retain_to_maturity_label,
            options=Menu.retain_to_maturity_options,
            key=key
        )
    
    @staticmethod
    def show_hold_in_days_input():
        return st.number_input(
            label=Text.maturity_hold_label,
            min_value=Operations.factor_base
        )
    
    @staticmethod
    def show_yield_input():
        return st.text_input(
            label=Text.yield_input_label
        )
    
    @staticmethod
    def show_liquid_title(liquid_title):
        return st.write(
            liquid_title,
            unsafe_allow_html=Settings.ALLOW_HTML
        )
