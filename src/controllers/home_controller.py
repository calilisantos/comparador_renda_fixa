from datetime import datetime
import streamlit as st

from configs.components import Menu, Text
from configs.inflation import InflationTypes
from domain.index_facade import IndexFacade
from domain.yield_facade import YieldFacade
from services.date import DateService
from services.inflation import InflationService
from views.home import HomeView
from views.metrics import MetricBuilder


class HomeController:
    def __init__(self):
        self.today = datetime.now()
        self.default_date = DateService(current_date=self.today).set_default_date()
        self.yields = IndexFacade(current_date=self.today).get_all_yields()
        self._prepare_base_yields()

    def _prepare_base_yields(self):
        self.cdi = self.yields.get(Text.cdi_label)
        self.selic = self.yields.get(Text.selic_label)
        self.poupanca = self.yields.get(Text.poupanca_label)

    def render(self):
        HomeView.show_main_title()
        product = HomeView.show_products_box()

        if product == Text.poupanca_label:
            self._render_poupanca_comparisons()
        else:
            self._render_fixed_income_flow(product)

    def _render_poupanca_comparisons(self):
        HomeView.show_result_title()
        cdi_col, selic_col = st.columns(Menu.columns_qty)
        poupanca_col, index_col = st.columns(Menu.columns_qty)

        for col, label, base in [
            (cdi_col, Text.cdi_label, self.cdi),
            (selic_col, Text.selic_label, self.selic),
            (poupanca_col, Text.poupanca_label, self.poupanca)
        ]:
            MetricBuilder.build_comparison(
                column=col, label=label,
                base_value=base,
                compared_value=self.poupanca
            )

        index_yield = InflationService(yields=self.yields).resolve_yield()
        MetricBuilder.build_index(
            column=index_col,
            index_yield=index_yield,
            compared_value=self.poupanca,
            label=Text.inflation_label,
            suffix=InflationTypes.DEFAULT
        )

    def _render_fixed_income_flow(self, product):
        bond_type = HomeView.show_bond_type_radio()

        if bond_type == Text.inflation_yield:
            index_type = HomeView.show_index_type_radio()
        else:
            index_type = InflationTypes.DEFAULT

        maturity_type = HomeView.show_maturity_type_radio()

        if maturity_type == Text.maturity_date_label:
            maturity_date = datetime.combine(
                date=HomeView.show_maturity_date_input(self.default_date),
                time=self.today.time()
            )
            maturity_days = (maturity_date - self.today).days
        elif maturity_type == Text.maturity_in_days:
            maturity_days = HomeView.show_maturity_in_days_input()
        else:
            maturity_days = (self.default_date - self.today).days

        if maturity_type != Text.unknown_maturity:
            hold_radio = HomeView.show_hold_until_maturity_radio()
            if hold_radio == Text.not_hold_to_maturity:
                maturity_days = HomeView.show_hold_in_days_input()

        yield_input = HomeView.show_yield_input()

        if not yield_input:
            return

        index_yield = InflationService(index_type=index_type, yields=self.yields).resolve_yield()

        yield_input, liquid_yield = YieldFacade(base_yields={
            "CDI": self.cdi,
            "SELIC": self.selic,
            "INFLATION": index_yield
        }).calculate(
            bond_type_label=bond_type,
            yield_input=yield_input,
            maturity_days=maturity_days,
            tax_free=(product == Text.credit_letters_label)
        )

        liquid_title = (
            Text.credit_letters_title.format(liquid_yield=liquid_yield, maturity_in_days=maturity_days, yield_input=yield_input)
            if product == Text.credit_letters_label
            else Text.liquid_yield_title.format(liquid_yield=liquid_yield, maturity_in_days=maturity_days)
        )

        HomeView.show_result_title()
        HomeView.show_liquid_title(liquid_title)

        cdi_col, selic_col = st.columns(Menu.columns_qty)
        poupanca_col, index_col = st.columns(Menu.columns_qty)

        for col, label, base in [
            (cdi_col, Text.cdi_label, self.cdi),
            (selic_col, Text.selic_label, self.selic),
            (poupanca_col, Text.poupanca_label, self.poupanca)
        ]:
            MetricBuilder.build_comparison(
                column=col,
                label=label,
                base_value=base,
                compared_value=yield_input
            )

        MetricBuilder.build_index(
            column=index_col,
            index_yield=index_yield,
            compared_value=yield_input,
            label=Text.inflation_label,
            suffix=index_type
        )
