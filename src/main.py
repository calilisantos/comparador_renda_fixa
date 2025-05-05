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
        'Letras de Crédito (LCA,LCI, LCD,...)',
        'Tesouro Direto',
        'Poupança',
        'Caixinha Nubank'
    ]
)

# """
# A depender do produto o input de investimento vai ser diferente
# Se pré-fixado 
# pós-fixado
# indexado
# """

bond_type = st.radio(
    label='Selecione o tipo de rendimento',
    options=[
        'Não sei',
        'Taxa Pré-fixada (ex: 10% a.a.)',
        # 'Taxa Pós-fixado ',
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

if maturity_type == 'Data de Vencimento':
    maturity_date = st.date_input(
        label='Data',
        # placeholder='dd/mm/yyyy',
        # value=None,
        # min_value=None,
        # max_value=None,
        # disabled=False,
        # help="Selecione a data de vencimento do produto"
    )
elif maturity_type == 'Prazo de Vencimento (em dias)':
    maturity_date = st.number_input(
        label='Informe o prazo de vencimento',
        # placeholder='ex: 30',
        min_value=1,
        # max_value=100,
        # value=10,
        # step=1
    )
elif maturity_type == 'Não sei':
    maturity_date = datetime.now() + timedelta(days=360)

# padronizar data para dias em relação a hoje


if bond_type == 'Taxa + Inflação (ex: 1% + IPCA)':
    index_type = st.radio(
        label='Selecione o tipo de indexador',
        options=[
            'IPCA',
            'IGPM',
            'INPC'
        ]
    )

# TODO:
# fazer lógica para cada um dos tipos:
# transformar em taxa anual
# caso especial para inflação? (ex: taxa% + IPCA)

fee_input = st.text_input(
    label='Informe a taxa de rendimento',
    # min_value=0.0,
    # max_value=100.0,
    # value=10.0,
    # step=0.1
)

if fee_input:
    fee_input = float(str(fee_input).replace(",", "."))

    # TODO: request para pegar esses dados
    cdi_fee = 14.39
    ipca_fee = 6.5
    selic_fee = 14.5
    igpm_fee = 5.0
    inpc_fee = 4.0

    tax_fees = .85

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