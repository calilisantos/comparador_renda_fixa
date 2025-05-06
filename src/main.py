from datetime import datetime, timedelta
import streamlit as st

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
        'Poupança', # Fazer fluxo para poupança. Não terá prazo nem taxa a informar
        'Caixinha Nubank'
    ]
)

free_tax_options = [
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

index_type = 'IPCA'
if bond_type == 'Taxa + Inflação (ex: 1% + IPCA)':
    index_type = st.radio(
        label='Selecione o tipo de indexador',
        options=[
            'IPCA',
            'IGPM',
            'INPC'
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

today = datetime.now()
default_date = today + timedelta(days=360)

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
elif maturity_type == 'Prazo de Vencimento (em dias)':
    maturity_in_days = st.number_input(
        label='Informe o prazo de vencimento',
        # placeholder='ex: 30',
        min_value=1,
        # max_value=100,
        # value=10,
        # step=1
    )
elif maturity_type == 'Não sei':
    maturity_date = default_date
    
if maturity_type is not 'Prazo de Vencimento (em dias)':
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
    fee_input = float(str(fee_input).replace(",", "."))

    # pós-fixada case:
    if bond_type == 'Taxa Pós-fixada (em porcentagem; ex: 90% do CDI)':
        fee_input = fee_input / 100

    # TODO:
    # adequar a maturidade para a taxa

    # request para pegar esses dados
    cdi_fee = 14.39
    ipca_fee = 6.5
    selic_fee = 14.5
    igpm_fee = 5.0
    inpc_fee = 4.0
    poupanca_fee = 6

    ## inflação case:
    index_dict = {
        'IPCA': ipca_fee,
        'IGPM': igpm_fee,
        'INPC': inpc_fee
    }

    index_fee = index_dict.get(index_type, 'IPCA')

    # fazer lógica para os N prazos de tributação e a data de vencimento
    if bond_type in free_tax_options:
        tax_fees = 0
    if maturity_in_days <= 180:
        tax_fees = 0.225
    elif maturity_in_days <= 360:
        tax_fees = 0.2
    elif maturity_in_days <= 720:
        tax_fees = 0.175
    else:
        tax_fees = 0.15

    if bond_type == 'Taxa Pré-fixada (ex: 10% a.a.)':
        liquid_fee = round(fee_input * (1 - tax_fees), 2)
    if bond_type == 'Taxa Pós-fixada (em porcentagem; ex: 90% do CDI)':
        liquid_fee = round((fee_input * cdi_fee) * (1 - tax_fees), 2)
    if bond_type == 'Taxa + CDI (ex: 1% + CDI)':
        liquid_fee = round((fee_input + cdi_fee) * (1 - tax_fees), 2)
    elif bond_type == 'Taxa + Selic (ex: 1% + Selic)':
        liquid_fee = round((fee_input + selic_fee) * (1 - tax_fees), 2)
    elif bond_type == 'Taxa + Inflação (ex: 1% + IPCA)':
        liquid_fee = round((fee_input + index_fee) * (1 - tax_fees), 2)

    # TODO:
    # calcular o rendimento líquido ou bruto? por enquanto líquido
    # booleano para aparecer as métricas se os inputs forem preenchidos

    st.write(
        f'<h2><center>Comparativo do Seu Produto</center></h2>',
        unsafe_allow_html=True
    )
    st.write(
        f'<h3><center>Rendimento Líquido: {liquid_fee}%</center></h3>',
        unsafe_allow_html=True
    )

    cdi_comparison, selic_comparison = st.columns(2) 
    poupanca_comparison, index_comparison = st.columns(2)
    cdi_comparison.metric(
        border=True,
        delta=f'{round(((liquid_fee-cdi_fee)/cdi_fee)*100, 2)}%',
        label='CDI',
        value=f'{cdi_fee}%'
    )
        
    selic_comparison.metric(
        border=True,
        delta=f'{round(((liquid_fee-selic_fee)/selic_fee)*100, 2)}%',
        label='Selic',
        value=f'{selic_fee}%',
    )

    poupanca_comparison.metric(
        border=True,
        delta=f'{round(((liquid_fee-poupanca_fee)/poupanca_fee)*100, 2)}%',
        label='Poupança',
        value=f'{poupanca_fee}%',
    )

    index_comparison.metric(
        border=True,
        # delta=f'{round((liquid_fee/(liquid_fee+ipca_fee)), 2)}%',
        label='Inflação', # comparar com NTN?
        value=f'{round(liquid_fee-index_fee, 2)}%+{index_type}'
    )
