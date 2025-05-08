from models.ratio_updates import Dates, DefaultValues, Operations, Request, Tax
from datetime import datetime, timedelta
from functools import reduce
from interfaces.components import Menu, Text
import requests
import streamlit as st


today = datetime.now()
def transform_date(days_diff, date_format=None):
    if date_format:
        past_day = today - timedelta(days=days_diff)
        return past_day.strftime(date_format)
    return today + timedelta(days=days_diff)

default_date = transform_date(days_diff=Dates.default_days_delay)

## Lógica do request

request_date_format = Dates.DATE_FORMAT
fees_request_date = transform_date(days_diff=Dates.fees_days_delay, date_format=request_date_format)
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
    cdi_fee = get_ratio(response=fetch_data(ratio_code=Request.cdi_code, request_date=fees_request_date),ratio_code=Request.cdi_code)
    selic_fee = get_ratio(response=fetch_data(ratio_code=Request.selic_code, request_date=fees_request_date),ratio_code=Request.selic_code)
    ipc_fee = get_ratio(response=fetch_data(ratio_code=Request.ipc_code, request_date=index_request_date),ratio_code=Request.ipc_code)
    ipca_fee = get_ratio(response=fetch_data(ratio_code=Request.ipca_code, request_date=index_request_date),ratio_code=Request.ipca_code)
    igpm_fee = get_ratio(response=fetch_data(ratio_code=Request.igpm_code, request_date=index_request_date),ratio_code=Request.igpm_code)
except:
    cdi_fee = DefaultValues.CDI_FEE
    selic_fee = DefaultValues.SELIC_FEE
    ipc_fee = DefaultValues.IPC_FEE
    ipca_fee = DefaultValues.IPCA_FEE
    igpm_fee = DefaultValues.IGPM_FEE


poupanca_fee = DefaultValues.POUPANCA_FEE
fee_input = poupanca_fee
index_fee = ipca_fee
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
        delta=f'{round(((fee_input-cdi_fee)/cdi_fee)*Operations.percent_value, Operations.round_value)}%',
        label=Text.cdi_label,
        value=f'{cdi_fee}%'
    )
        
    selic_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-selic_fee)/selic_fee)*Operations.percent_value, Operations.round_value)}%',
        label=Text.selic_label,
        value=f'{selic_fee}%',
    )

    poupanca_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-poupanca_fee)/poupanca_fee)*Operations.percent_value, Operations.round_value)}%',
        label=Text.poupanca_label,
        value=f'{poupanca_fee}%',
    )

    index_comparison.metric(
        border=True,
        label=Text.inflation_label, # comparar com NTN?
        value=f'{round(fee_input-index_fee, Operations.round_value)}%+{index_type}'
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

    fee_input = st.text_input(
        label=Text.fee_input_label
    )

    # submitted = st.form_submit_button("Comparar Produto")

    # if submitted and fee_input:
    if fee_input:
        index_dict = {
            DefaultValues.INDEX_TYPE: ipca_fee,
            Text.igpm_label: igpm_fee,
            Text.ipc_label: ipc_fee
        }

        index_fee = index_dict.get(index_type, DefaultValues.INDEX_TYPE)

        fee_input = float(str(fee_input).replace(",", "."))
        
        bond_fee_by_type = {
            Text.post_fixed_option_label: (fee_input / Operations.percent_value) * cdi_fee,
            Text.cdi_option_label: fee_input + cdi_fee,
            Text.selic_option_label: fee_input + selic_fee,
            Text.inflation_option_label: fee_input + index_fee
        }

        fee_input = bond_fee_by_type.get(bond_type, fee_input)

        if product == Text.credit_letters_label:
            tax_fees = Tax.free_tax
        elif maturity_in_days <= Tax.semester_range:
            tax_fees = Tax.semester_fee
        elif maturity_in_days <= Tax.anual_range:
            tax_fees = Tax.anual_fee
        elif maturity_in_days <= Tax.bianual_range:
            tax_fees = Tax.bianual_fee
        else:
            tax_fees = Tax.beyond_fee

        liquid_fee = round(fee_input * (Operations.factor_base - tax_fees), Operations.round_value)

        st.write(
            Text.result_title,
            unsafe_allow_html=True
        )
        st.write(
            Text.liquid_fee_title.format(liquid_fee=liquid_fee, maturity_in_days=maturity_in_days),
            unsafe_allow_html=True
        )

        cdi_comparison, selic_comparison = st.columns(Menu.columns_qty) 
        poupanca_comparison, index_comparison = st.columns(Menu.columns_qty)
        cdi_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-cdi_fee)/cdi_fee)*Operations.percent_value, Operations.round_value)}%',
            label=Text.cdi_label,
            value=f'{cdi_fee}%'
        )
            
        selic_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-selic_fee)/selic_fee)*Operations.percent_value, Operations.round_value)}%',
            label=Text.selic_label,
            value=f'{selic_fee}%',
        )

        poupanca_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-poupanca_fee)/poupanca_fee)*Operations.percent_value, Operations.round_value)}%',
            label=Text.poupanca_label,
            value=f'{poupanca_fee}%',
        )

        index_comparison.metric(
            border=True,
            label=Text.inflation_label,
            value=f'{round(fee_input-index_fee, Operations.round_value)}%+{index_type}'
        )
