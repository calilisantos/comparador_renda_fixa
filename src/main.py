from models.dates import Dates
from models.yields import DefaultValues, Operations, Tax
from models.request import Request
from datetime import datetime, timedelta
from functools import reduce
from interfaces.components import Menu, Text
import requests
import streamlit as st


today = datetime.now() # deixar na main ou controller. É usada no request e no deal com data de vencimento
def transform_date(days_diff, date_format=None):
    if date_format:
        past_day = today - timedelta(days=days_diff)
        return past_day.strftime(date_format)
    return today + timedelta(days=days_diff)

default_date = transform_date(days_diff=Dates.default_days_delay)

## Lógica do request

request_date_format = Dates.DATE_FORMAT
yields_request_date = transform_date(days_diff=Dates.yields_days_delay, date_format=request_date_format)
index_request_date = transform_date(days_diff=Dates.inflation_days_delay, date_format=request_date_format)


def fetch_data(ratio_code, request_date):
    #função para o request - OK; outra para tratar a resposta - Refatorar; outra para converter a taxa para ano - Criar?
    response = requests.get(Request.bacen_endpoint.format(ratio_code=ratio_code, request_date=request_date))
    response.raise_for_status()
    return response.json()

def get_ratio(response,ratio_code):
    if ratio_code == Request.selic_code:
        return float(response[Request.response_index].get(Request.ratio_key))  # para selic (que é anual)
    elif ratio_code == Request.cdi_code:
        value = float(response[Request.response_index].get(Request.ratio_key)) / Operations.percent_value
        return round((((Operations.factor_base + value) ** Operations.util_days) -Operations.factor_base) * Operations.percent_value, Operations.round_value)
    else:
        compound_value = reduce(
            lambda acc, curr: (((Operations.factor_base + (acc/Operations.percent_value)) * (Operations.factor_base + (float(curr[Request.ratio_key]) / Operations.percent_value)))-Operations.factor_base)*Operations.percent_value,
            response[-Request.response_range:],
            Operations.reduce_initial
        )
        return round(compound_value, Operations.round_value) # para inflação que são acumulado mensal

try:
    cdi_yield = get_ratio(response=fetch_data(ratio_code=Request.cdi_code, request_date=yields_request_date),ratio_code=Request.cdi_code)
    selic_yield = get_ratio(response=fetch_data(ratio_code=Request.selic_code, request_date=yields_request_date),ratio_code=Request.selic_code)
    ipc_yield = get_ratio(response=fetch_data(ratio_code=Request.ipc_code, request_date=index_request_date),ratio_code=Request.ipc_code)
    ipca_yield = get_ratio(response=fetch_data(ratio_code=Request.ipca_code, request_date=index_request_date),ratio_code=Request.ipca_code)
    igpm_yield = get_ratio(response=fetch_data(ratio_code=Request.igpm_code, request_date=index_request_date),ratio_code=Request.igpm_code)
except:
    cdi_yield = DefaultValues.CDI_YIELD
    selic_yield = DefaultValues.SELIC_YIELD
    ipc_yield = DefaultValues.IPC_YIELD
    ipca_yield = DefaultValues.IPCA_YIELD
    igpm_yield = DefaultValues.IGPM_YIELD


poupanca_yield = DefaultValues.POUPANCA_YIELD
yield_input = poupanca_yield
index_yield = ipca_yield
index_type = DefaultValues.INDEX_TYPE


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
        index_dict = {
            DefaultValues.INDEX_TYPE: ipca_yield,
            Text.igpm_label: igpm_yield,
            Text.ipc_label: ipc_yield
        }

        index_yield = index_dict.get(index_type, DefaultValues.INDEX_TYPE)

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
