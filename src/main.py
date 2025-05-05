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
        'Poupança',
        'Caixinha Nubank'
    ]
)

bond_type = st.radio(
    label='Selecione o tipo de rendimento',
    options=[
        # 'Não sei',
        'Taxa Pré-fixada (ex: 10% a.a.)',
        'Taxa Pós-fixada (ex: 90% do CDI)',
        'Taxa + CDI (ex: 1% + CDI)',
        'Taxa + Selic (ex: 1% + Selic)',
        'Taxa + Inflação (ex: 1% + IPCA)',
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
    
# st.write(f"maturity_in_days: {maturity_in_days}, maturity_in_days type: {type(maturity_in_days)}")


if bond_type == 'Taxa + Inflação (ex: 1% + IPCA)':
    index_type = st.radio(
        label='Selecione o tipo de indexador',
        options=[
            'IPCA',
            'IGPM',
            'INPC'
        ]
    )

fee_input = st.text_input(
    label='Informe a taxa de rendimento',
    # min_value=0.0,
    # max_value=100.0,
    # value=10.0,
    # step=0.1
)

if fee_input:
    fee_input = float(str(fee_input).replace(",", "."))

    # TODO:
    # fazer lógica para cada um dos tipos:
    # transformar em taxa anual
    # caso especial para inflação? (ex: taxa% + IPCA)

    # request para pegar esses dados
    cdi_fee = 14.39
    ipca_fee = 6.5
    selic_fee = 14.5
    igpm_fee = 5.0
    inpc_fee = 4.0

    # fazer lógica para os N prazos de tributação e a data de vencimento
    tax_fees = 0
    # if maturity_in_days <= 180:
    #     tax_fees = 0.225
    # elif maturity_in_days <= 360:
    #     tax_fees = 0.2
    # elif maturity_in_days <= 720:
    #     tax_fees = 0.175
    # else:
    #     tax_fees = 0.15

    if bond_type is not 'Taxa Pré-fixada (ex: 10% a.a.)':
        if bond_type == 'Taxa Pós-fixada (ex: 90% do CDI)':
            liquid_fee = (fee_input * cdi_fee) * (1 - tax_fees)
        if bond_type == 'Taxa + CDI (ex: 1% + CDI)':
            liquid_fee = (fee_input + cdi_fee) * (1 - tax_fees)
        elif bond_type == 'Taxa + Selic (ex: 1% + Selic)':
            liquid_fee = (fee_input + selic_fee) * (1 - tax_fees)
        elif bond_type == 'Taxa + Inflação (ex: 1% + IPCA)':
            if index_type == 'IPCA':
                liquid_fee = (fee_input + ipca_fee) * (1 - tax_fees)
            elif index_type == 'IGPM':
                liquid_fee = (fee_input + igpm_fee) * (1 - tax_fees)
            elif index_type == 'INPC':
                liquid_fee = (fee_input + inpc_fee) * (1 - tax_fees)

    # TODO:
    # calcular o rendimento líquido ou bruto?
    # booleano para aparecer as métricas se os inputs forem preenchidos

    st.write(
        f'<h2><center>Comparativo do Seu Produto</center></h2>',
        unsafe_allow_html=True
    )
    # ajustar lógica do delta
    cdi_comparison, selic_comparison, index_comparison = st.columns(3)
    cdi_comparison.metric(
        label='CDI',
        value=f'{cdi_fee}%',
        delta=f'{round((fee_input/cdi_fee), 2)}%'
    )
        
    selic_comparison.metric(
        label='Selic',
        value=f'{selic_fee}%',
        delta=f'{round((fee_input/selic_fee), 2)}%'
    )

    # ajustar caso do indexador
    index_comparison.metric(
        label='Inflação',
        value=f'{ipca_fee}%',
        delta=f'{round((fee_input/(fee_input+ipca_fee)), 2)}%'
    )