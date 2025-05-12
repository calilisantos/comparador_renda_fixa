from datetime import datetime
import streamlit as st
from configs.components import Menu, Text
from configs.inflation import InflationTypes
from configs.yield_types import YieldType
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
        self.base_fields = {
            YieldType.CDI.base_key(): self.yields.get(Text.cdi_label),
            YieldType.SELIC.base_key(): self.yields.get(Text.selic_label),
            YieldType.INFLATION.base_key(): InflationService(yields=self.yields).resolve_yield()
        }

    def run(self):
        HomeView.show_main_title()
        product = HomeView.show_products_box()

        if product == Text.poupanca_label:
            self._handle_poupanca()
        else:
            self._handle_yield_comparison(product)

    def _build_metrics(self, compared_yield, index_type=InflationTypes.DEFAULT):
        cdi_col, selic_col = st.columns(Menu.columns_qty)
        poupanca_col, index_col = st.columns(Menu.columns_qty)

        MetricBuilder.build_comparison(cdi_col, self.base_fields["CDI"], compared_yield, Text.cdi_label)
        MetricBuilder.build_comparison(selic_col, self.base_fields["SELIC"], compared_yield, Text.selic_label)
        MetricBuilder.build_comparison(poupanca_col, self.yields.get(Text.poupanca_label), compared_yield, Text.poupanca_label)
        MetricBuilder.build_index(index_col, self.base_fields["INFLATION"], compared_yield, Text.inflation_label, suffix=index_type)


    def _handle_poupanca(self):
        HomeView.show_result_title()

        yield_input = self.yields.get(Text.poupanca_label)
        self._build_metrics(compared_yield=yield_input)

    def _handle_yield_comparison(self, product):
        bond_type = HomeView.show_bond_type_radio()
        index_type = InflationTypes.DEFAULT

        if bond_type == Text.inflation_yield:
            index_type = HomeView.show_index_type_radio()

        maturity_in_days = self._get_maturity_in_days()

        yield_input = HomeView.show_yield_input()

        if yield_input:
            try:
                self.base_fields["INFLATION"] = InflationService(index_type=index_type, yields=self.yields).resolve_yield()
                is_tax_free = product == Text.credit_letters_label

                gross_yield, net_yield = YieldFacade(base_yields=self.base_fields).calculate(
                    bond_type_label=bond_type,
                    yield_input=yield_input,
                    maturity_days=maturity_in_days,
                    tax_free=is_tax_free
                )

                HomeView.show_result_title()
                HomeView.show_liquid_title(
                    Text.credit_letters_title.format(liquid_yield=net_yield, maturity_in_days=maturity_in_days, yield_input=gross_yield)
                    if is_tax_free
                    else Text.liquid_yield_title.format(liquid_yield=net_yield, maturity_in_days=maturity_in_days)
                )

                self._build_metrics(compared_yield=gross_yield, index_type=index_type)
            except ValueError:
                st.error(Text.invalid_yield_message)

    def _get_maturity_in_days(self):
        maturity_type = HomeView.show_maturity_type_radio()

        if maturity_type == Text.maturity_date_label:
            maturity_date = datetime.combine(
                date=HomeView.show_maturity_date_input(default_date=self.default_date),
                time=self.today.time()
            )
            maturity_in_days = (maturity_date - self.today).days

        elif maturity_type == Text.maturity_in_days:
            maturity_in_days = HomeView.show_maturity_in_days_input()

        else:
            unknown_date = DateService(current_date=self.today).set_unknown_maturity_date()
            return (unknown_date - self.today).days

        hold_key = f"hold_until_maturity_{maturity_type}"
        hold_until_maturity = HomeView.show_hold_until_maturity_radio(key=hold_key)
        if hold_until_maturity == Text.not_hold_to_maturity:
            return HomeView.show_hold_in_days_input()

        return maturity_in_days
