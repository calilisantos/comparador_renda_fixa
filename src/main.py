from domain.yield_facade import YieldFacade
from models.yields import Operations, Tax
from services.date import DateService
from services.inflation import InflationService
from datetime import datetime
from interfaces.components import Menu, Text
import streamlit as st


today = datetime.now() # ver aonde colocar. É usada no request e no deal com data de vencimento

default_date = DateService(current_date=today).set_default_date() # é usada em maturity_date. tirar daqui

yields = YieldFacade(current_date=today).get_all_yields()
cdi_yield = yields["cdi"]
selic_yield = yields["selic"]
poupanca_yield = yields["poupanca"]

yield_input = poupanca_yield
index_type = Text.ipca_label
index_yield = InflationService(yields=yields).resolve_yield()


# Lógica do app

st.write(
    Text.main_title,
    unsafe_allow_html=True
)

product = st.selectbox(
    label=Text.product_label,
    options=Menu.product_options
)

if product == Text.poupanca_label:
    st.write(
        Text.comparative_title,
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
        label=Text.inflation_label, # comparar com NTN?
        value=f'{round(yield_input-index_yield, Operations.round_value)}%+{index_type}'
    )
else:
    # with st.form(key="bond_form"):
    bond_type = st.radio(
        label=Text.yield_title,
        options=Menu.yield_options
    )

    if bond_type == Text.inflation_yield:
        index_type = st.radio(
            label=Text.inflation_index_label,
            options=Menu.inflation_index_options
        )

    maturity_type = st.radio(
        label=Text.maturity_label,
        options=Menu.maturity_options
    )

    if maturity_type == Text.maturity_date_label:
        maturity_date = datetime.combine(
            date=st.date_input(
                label=Text.date_label,
                format=Text.date_input_format,
                value=default_date
            ),
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

        yield_input = float(str(yield_input).replace(",", "."))
        
        bond_yield_by_type = {
            Text.post_fixed_option_label: (yield_input / Operations.percent_value) * cdi_yield,
            Text.cdi_option_label: yield_input + cdi_yield,
            Text.selic_option_label: yield_input + selic_yield,
            Text.inflation_option_label: yield_input + index_yield
        }

        yield_input = bond_yield_by_type.get(bond_type, yield_input)

        if maturity_in_days <= Tax.semester_range:
            tax_yields = Tax.semester_yield
        elif maturity_in_days <= Tax.anual_range:
            tax_yields = Tax.anual_yield
        elif maturity_in_days <= Tax.bianual_range:
            tax_yields = Tax.bianual_yield
        else:
            tax_yields = Tax.beyond_yield

        def set_tax_adjusted(yield_value, tax_yield):
            return round(yield_value * (Operations.factor_base - tax_yield), Operations.round_value)

        if product == Text.credit_letters_label:
            liquid_yield = set_tax_adjusted(yield_value=yield_input, tax_yield=Tax.free_tax)
            yield_input = set_tax_adjusted(yield_value=yield_input, tax_yield=-tax_yields)
            liquid_title = Text.credit_letters_title.format(liquid_yield=liquid_yield, maturity_in_days=maturity_in_days, yield_input=yield_input)
        else:
            liquid_yield = set_tax_adjusted(yield_value=yield_input, tax_yield=tax_yields)
            liquid_title = Text.liquid_yield_title.format(liquid_yield=liquid_yield, maturity_in_days=maturity_in_days)

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
