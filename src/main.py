from config.ratio_updates import Dates, Operations, Request
from datetime import datetime, timedelta
from functools import reduce
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
        return round((((Operations.factor_base + value) ** 252) -Operations.factor_base) * Operations.percent_value, Operations.round_value)
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
    cdi_fee = 14.39
    selic_fee = 14.5
    ipc_fee = 4.0
    ipca_fee = 6.5
    igpm_fee = 5.0


poupanca_fee = 6.17
fee_input = poupanca_fee
index_fee = ipca_fee
index_type = 'IPCA'


# Lógica do app

st.write(
    f'<h1><center>Comparador de Renda Fixa</center></h1>',
    unsafe_allow_html=True
)

product = st.selectbox(
    label='Selecione seu produto',
    options=[
        'CDB',
        'Debênture',
        'Letras de Crédito (LCA,LCI, LCD,...)',
        'Tesouro Direto',
        'Poupança',
        'Caixinha Nubank'
    ]
)

if product == 'Poupança':
    st.write(
        f'<h2><center>Comparativo do Seu Produto</center></h2>',
        unsafe_allow_html=True
    )

    cdi_comparison, selic_comparison = st.columns(2) 
    poupanca_comparison, index_comparison = st.columns(2)
    cdi_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-cdi_fee)/cdi_fee)*Operations.percent_value, Operations.round_value)}%',
        label='CDI',
        value=f'{cdi_fee}%'
    )
        
    selic_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-selic_fee)/selic_fee)*Operations.percent_value, Operations.round_value)}%',
        label='Selic',
        value=f'{selic_fee}%',
    )

    poupanca_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-poupanca_fee)/poupanca_fee)*Operations.percent_value, Operations.round_value)}%',
        label='Poupança',
        value=f'{poupanca_fee}%',
    )

    index_comparison.metric(
        border=True,
        label='Inflação', # comparar com NTN?
        value=f'{round(fee_input-index_fee, Operations.round_value)}%+{index_type}'
    )
else:
    # with st.form(key="bond_form"):
    bond_type = st.radio(
        label='Selecione o tipo de rendimento',
        options=[
            # 'Não sei',
            'Taxa Pré-fixada (ex: 10% a.a.)',
            'Taxa Pós-fixada (em porcentagem; ex: 90% do CDI)',
            'Taxa + CDI (ex: 1% + CDI)',
            'Taxa + Selic (ex: 1% + Selic)',
            'Taxa + Inflação (ex: 1% + IPCA)',
        ]
    )

    if bond_type == 'Taxa + Inflação (ex: 1% + IPCA)':
        index_type = st.radio(
            label='Selecione o tipo de indexador',
            options=[
                'IPCA',
                'IGPM',
                'IPC'
            ]
        )

    maturity_type = st.radio(
        label='Informe a data de vencimento',
        options=[
            'Não sei',
            'Data de Vencimento',
            'Prazo de Vencimento (em dias)'
        ]
    )

    if maturity_type == 'Data de Vencimento':
        maturity_date = datetime.combine(
            date=st.date_input(
                label='Data',
                format='DD/MM/YYYY',
                value=default_date
            ),
            time=today.time()
        )
        maturity_in_days = (maturity_date - today).days
    elif maturity_type == 'Prazo de Vencimento (em dias)':
        maturity_in_days = st.number_input(
            label='Informe o prazo de vencimento (em dias)',
            min_value=1
        )
    else:
        maturity_date = default_date
        maturity_in_days = (maturity_date - today).days

    if maturity_type != 'Não sei':
        hold_until_maturity = st.radio(
            label='Você pretende manter até o vencimento?',
            options=[
                'Sim',
                'Não'
            ]
        )
        if hold_until_maturity == 'Não':
            maturity_in_days = st.number_input(
                label='Informe o tempo que pretende manter o produto (em dias)',
                min_value=1
            )

    fee_input = st.text_input(
        label='Informe a taxa de rendimento (ou taxa de referência para o pós-fixado: ex. 95,3 para 95,3% CDI)'
    )

    # submitted = st.form_submit_button("Comparar Produto")

    # if submitted and fee_input:
    if fee_input:
        index_dict = {
            'IPCA': ipca_fee,
            'IGPM': igpm_fee,
            'IPC': ipc_fee
        }

        index_fee = index_dict.get(index_type, 'IPCA')

        fee_input = float(str(fee_input).replace(",", "."))
        
        bond_fee_by_type = {
            'Taxa Pós-fixada (em porcentagem; ex: 90% do CDI)': (fee_input / Operations.percent_value) * cdi_fee,
            'Taxa + CDI (ex: 1% + CDI)': fee_input + cdi_fee,
            'Taxa + Selic (ex: 1% + Selic)': fee_input + selic_fee,
            'Taxa + Inflação (ex: 1% + IPCA)': fee_input + index_fee
        }

        fee_input = bond_fee_by_type.get(bond_type, fee_input)

        if product == 'Letras de Crédito (LCA,LCI, LCD,...)':
            tax_fees = 0
        elif maturity_in_days <= 180:
            tax_fees = 0.225
        elif maturity_in_days <= 360:
            tax_fees = 0.2
        elif maturity_in_days <= 720:
            tax_fees = 0.175
        else:
            tax_fees = 0.15

        liquid_fee = round(fee_input * (1 - tax_fees), Operations.round_value)

        st.write(
            f'<h2><center>Comparativo do Seu Produto</center></h2>',
            unsafe_allow_html=True
        )
        st.write(
            f'<p><h3><center>Rendimento Líquido: {liquid_fee}%*</p> <p>*Com o resgate em {maturity_in_days} dias</p></center></h3>',
            unsafe_allow_html=True
        )

        cdi_comparison, selic_comparison = st.columns(2) 
        poupanca_comparison, index_comparison = st.columns(2)
        cdi_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-cdi_fee)/cdi_fee)*Operations.percent_value, Operations.round_value)}%',
            label='CDI',
            value=f'{cdi_fee}%'
        )
            
        selic_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-selic_fee)/selic_fee)*Operations.percent_value, Operations.round_value)}%',
            label='Selic',
            value=f'{selic_fee}%',
        )

        poupanca_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-poupanca_fee)/poupanca_fee)*Operations.percent_value, Operations.round_value)}%',
            label='Poupança',
            value=f'{poupanca_fee}%',
        )

        index_comparison.metric(
            border=True,
            label='Inflação',
            value=f'{round(fee_input-index_fee, Operations.round_value)}%+{index_type}'
        )
