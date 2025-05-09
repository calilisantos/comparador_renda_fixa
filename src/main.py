from domain.index_facade import IndexFacade
from domain.yield_facade import YieldFacade
from configs.inflation import InflationTypes
from models.yields import Operations
from services.date import DateService
from services.inflation import InflationService
from datetime import datetime
from configs.components import Menu, Text
import streamlit as st
from views.home import HomeView
from views.metrics import MetricBuilder


today = datetime.now() # ver aonde colocar. É usada no request e no deal com data de vencimento

default_date = DateService(current_date=today).set_default_date() # é usada em maturity_date. tirar daqui

yields = IndexFacade(current_date=today).get_all_yields()
cdi_yield = yields.get(Text.cdi_label)
selic_yield = yields.get(Text.selic_label)
poupanca_yield = yields.get(Text.poupanca_label)

yield_input = poupanca_yield
index_type = InflationTypes.DEFAULT
index_yield = InflationService(yields=yields).resolve_yield()


# Lógica do app

HomeView.show_main_title()

product = HomeView.show_products_box()

if product == Text.poupanca_label:
    HomeView.show_result_title()

    cdi__metric_delta = f'{round(((yield_input-cdi_yield)/cdi_yield)*Operations.percent_value, Operations.round_value)}%'

    cdi_comparison, selic_comparison = st.columns(Menu.columns_qty) 
    poupanca_comparison, index_comparison = st.columns(Menu.columns_qty)

    MetricBuilder.build_comparison(
        column=cdi_comparison,
        base_value=cdi_yield,
        compared_value=yield_input,
        label=Text.cdi_label
    )
        
    MetricBuilder.build_comparison(
        column=selic_comparison,
        base_value=selic_yield,
        compared_value=yield_input,
        label=Text.selic_label
    )

    MetricBuilder.build_comparison(
        column=poupanca_comparison,
        base_value=poupanca_yield,
        compared_value=yield_input,
        label=Text.poupanca_label
    )

    MetricBuilder.build_index(
        column=index_comparison,
        index_yield=index_yield,
        compared_value=yield_input,
        label=Text.inflation_label,
        suffix=index_type
    )

else:
    bond_type = HomeView.show_bond_type_radio()

    if bond_type == Text.inflation_yield:
        index_type = HomeView.show_index_type_radio()

    maturity_type = HomeView.show_maturity_type_radio()

    if maturity_type == Text.maturity_date_label:
        maturity_date = datetime.combine(
            date= HomeView.maturity_date_input(default_date=default_date),
            time=today.time()
        )
        maturity_in_days = (maturity_date - today).days
    elif maturity_type == Text.maturity_in_days:
        maturity_in_days = st.number_input(
            label=Text.days_maturity_label,
            min_value=Operations.factor_base
        )
    else:
        maturity_date = default_date
        maturity_in_days = (maturity_date - today).days

    if maturity_type != Text.unknown_maturity:
        hold_until_maturity = st.radio(
            label=Text.retain_to_maturity_label,
            options=Menu.retain_to_maturity_options
        )
        if hold_until_maturity == Text.not_hold_to_maturity:
            maturity_in_days = st.number_input(
                label=Text.maturity_hold_label,
                min_value=Operations.factor_base
            )

    yield_input = st.text_input(
        label=Text.yield_input_label
    )

    # submitted = st.form_submit_button("Comparar Produto")

    # if submitted and yield_input:
    if yield_input:
        index_yield = InflationService(index_type=index_type, yields=yields).resolve_yield()

        base_fields = {
            "CDI": cdi_yield,
            "SELIC": selic_yield,
            "INFLATION": index_yield
        }

        is_tax_free = product == Text.credit_letters_label

        yield_input, liquid_yield = YieldFacade(base_yields=base_fields).calculate(
            bond_type_label=bond_type, 
            yield_input=yield_input, 
            maturity_days=maturity_in_days, 
            tax_free=is_tax_free
        )

        liquid_title = (
            Text.credit_letters_title.format(liquid_yield=liquid_yield, maturity_in_days=maturity_in_days, yield_input=yield_input) 
            if is_tax_free
            else Text.liquid_yield_title.format(liquid_yield=liquid_yield, maturity_in_days=maturity_in_days)
        )
        
        st.write(
            Text.result_title,
            unsafe_allow_html=True
        )

        st.write(
            liquid_title,
            unsafe_allow_html=True
        )

        cdi_comparison, selic_comparison = st.columns(Menu.columns_qty) 
        poupanca_comparison, index_comparison = st.columns(Menu.columns_qty)
        cdi_comparison.metric(
            border=True,
            delta=f'{round(((yield_input-cdi_yield)/cdi_yield)*Operations.percent_value, Operations.round_value)}%',
            label=Text.cdi_label,
            value=f'{cdi_yield}%'
        )
            
        selic_comparison.metric(
            border=True,
            delta=f'{round(((yield_input-selic_yield)/selic_yield)*Operations.percent_value, Operations.round_value)}%',
            label=Text.selic_label,
            value=f'{selic_yield}%',
        )

        poupanca_comparison.metric(
            border=True,
            delta=f'{round(((yield_input-poupanca_yield)/poupanca_yield)*Operations.percent_value, Operations.round_value)}%',
            label=Text.poupanca_label,
            value=f'{poupanca_yield}%',
        )

        index_comparison.metric(
            border=True,
            label=Text.inflation_label,
            value=f'{round(yield_input-index_yield, Operations.round_value)}%+{index_type}'
        )
