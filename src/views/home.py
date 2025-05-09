from configs.components import Menu, Settings, Text
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
    def maturity_date_input(default_date):
        return st.date_input(
            label=Text.date_label,
            format=Text.date_input_format,
            value=default_date
        )
