from datetime import datetime, timedelta
from functools import reduce
import requests
import streamlit as st


today = datetime.now()
default_date = today + timedelta(days=360)




## Lógica do request
request_date_format = "%d/%m/%Y"
yesterday = today - timedelta(days=1)
endpoint = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{ratio_code}/dados?formato=json&dataInicial={request_date}"

last_year = today - timedelta(days=390)
fees_request_date = yesterday.strftime(request_date_format)
index_request_date = last_year.strftime(request_date_format)

cdi_code = 12 # 4391
selic_code = 432 # 11 diário
ipc_code = 7465
ipca_code = 433
igpm_code = 189


def fetch_data(ratio_code, request_date):
    #função para o request - OK; outra para tratar a resposta - Refatorar; outra para converter a taxa para ano - Criar?
    response = requests.get(endpoint.format(ratio_code=ratio_code, request_date=request_date))
    response.raise_for_status()
    return response.json()

def get_ratio(response,ratio_code):
    if ratio_code == selic_code:
        return float(response[-1].get("valor"))  # para selic (que é anual)
    elif ratio_code == cdi_code:
        value = float(response[-1].get("valor")) / 100
        return round((((1 + value) ** 252) -1) * 100, 2) # para CDI (que é diário)
    else:
        compound_value = reduce(
            lambda acc, curr: (((1 + (acc/100)) * (1 + (float(curr["valor"]) / 100)))-1)*100,
            response[-12:],
            0
        )
        return round(compound_value, 2) # para inflação que são acumulado mensal

try:
    cdi_fee = get_ratio(response=fetch_data(ratio_code=cdi_code, request_date=fees_request_date),ratio_code=cdi_code)
    selic_fee = get_ratio(response=fetch_data(ratio_code=selic_code, request_date=fees_request_date),ratio_code=selic_code)
    ipc_fee = get_ratio(response=fetch_data(ratio_code=ipc_code, request_date=index_request_date),ratio_code=ipc_code)
    ipca_fee = get_ratio(response=fetch_data(ratio_code=ipca_code, request_date=index_request_date),ratio_code=ipca_code)
    igpm_fee = get_ratio(response=fetch_data(ratio_code=igpm_code, request_date=index_request_date),ratio_code=igpm_code)
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
        delta=f'{round(((fee_input-cdi_fee)/cdi_fee)*100, 2)}%',
        label='CDI',
        value=f'{cdi_fee}%'
    )
        
    selic_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-selic_fee)/selic_fee)*100, 2)}%',
        label='Selic',
        value=f'{selic_fee}%',
    )

    poupanca_comparison.metric(
        border=True,
        delta=f'{round(((fee_input-poupanca_fee)/poupanca_fee)*100, 2)}%',
        label='Poupança',
        value=f'{poupanca_fee}%',
    )

    index_comparison.metric(
        border=True,
        # delta=f'{round((liquid_fee/(liquid_fee+ipca_fee)), 2)}%',
        label='Inflação', # comparar com NTN?
        value=f'{round(fee_input-index_fee, 2)}%+{index_type}'
    )
else:
    free_tax_products = [
        'Letras de Crédito (LCA,LCI, LCD,...)',
        'Poupança'
    ]

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
                # placeholder='dd/mm/yyyy',
                # value=None,
                # min_value=None,
                # max_value=None,
                # disabled=False,
                # help="Selecione a data de vencimento do produto"
            ),
            time=today.time()
        )
        maturity_in_days = (maturity_date - today).days
    elif maturity_type == 'Prazo de Vencimento (em dias)':
        maturity_in_days = st.number_input(
            label='Informe o prazo de vencimento (em dias)',
            # placeholder='ex: 30',
            min_value=1,
            # max_value=100,
            # value=10,
            # step=1
        )
    elif maturity_type == 'Não sei':
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
                # placeholder='ex: 30',
                min_value=1,
                # max_value=100,
                # value=10,
                # step=1
            )
        
    # st.write(f"maturity_in_days: {maturity_in_days}, maturity_in_days type: {type(maturity_in_days)}")

    fee_input = st.text_input(
        label='Informe a taxa de rendimento (ou taxa de referência para o pós-fixado: ex. 95,3 para 95,3% CDI)',
        # min_value=0.0,
        # max_value=100.0,
        # value=10.0,
        # step=0.1
    )

    if fee_input:

        ## inflação case:
        index_dict = {
            'IPCA': ipca_fee,
            'IGPM': igpm_fee,
            'IPC': ipc_fee
        }

        index_fee = index_dict.get(index_type, 'IPCA')

        fee_input = float(str(fee_input).replace(",", "."))
        
        bond_fee_by_type = {
            'Taxa Pós-fixada (em porcentagem; ex: 90% do CDI)': (fee_input / 100) * cdi_fee,
            'Taxa + CDI (ex: 1% + CDI)': fee_input + cdi_fee,
            'Taxa + Selic (ex: 1% + Selic)': fee_input + selic_fee,
            'Taxa + Inflação (ex: 1% + IPCA)': fee_input + index_fee
        }
        fee_input = bond_fee_by_type.get(bond_type, fee_input)

        # fazer lógica para os N prazos de tributação e a data de vencimento
        if product in free_tax_products:
            tax_fees = 0
        elif maturity_in_days <= 180:
            tax_fees = 0.225
        elif maturity_in_days <= 360:
            tax_fees = 0.2
        elif maturity_in_days <= 720:
            tax_fees = 0.175
        else:
            tax_fees = 0.15

        liquid_fee = round(fee_input * (1 - tax_fees), 2)

        # TODO:
        # booleano para aparecer as métricas se os inputs forem preenchidos

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
            delta=f'{round(((fee_input-cdi_fee)/cdi_fee)*100, 2)}%',
            label='CDI',
            value=f'{cdi_fee}%'
        )
            
        selic_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-selic_fee)/selic_fee)*100, 2)}%',
            label='Selic',
            value=f'{selic_fee}%',
        )

        poupanca_comparison.metric(
            border=True,
            delta=f'{round(((fee_input-poupanca_fee)/poupanca_fee)*100, 2)}%',
            label='Poupança',
            value=f'{poupanca_fee}%',
        )

        index_comparison.metric(
            border=True,
            # delta=f'{round((liquid_fee/(liquid_fee+ipca_fee)), 2)}%',
            label='Inflação', # comparar com NTN?
            value=f'{round(fee_input-index_fee, 2)}%+{index_type}'
        )
