from configs.inflation import InflationTypes


class Text:
    cdi_label = 'CDI'
    cdi_option_label = 'Taxa + CDI (ex: 1% + CDI)'
    credit_letters_label = 'Letras de Crédito (LCA,LCI, LCD,...)'
    credit_letters_title = '<p><h3><center>Rendimento Líquido: {liquid_yield}%*</p> <p><strong>Rendimento equivalente {yield_input}%**</strong></p> <p>*Com o resgate em {maturity_in_days} dias</p> <p>**Considerando a compensação tributária. Usado no comparativo abaixo:</p></center></h3>'
    date_input_format = 'DD/MM/YYYY'
    date_label = 'Data'
    days_maturity_label = 'Informe o prazo de vencimento (em dias)'
    yield_input_label = 'Informe a taxa de rendimento (ou taxa de referência para o pós-fixado: ex. 95,3 para 95,3% CDI)'
    inflation_index_label = 'Selecione o tipo de indexador'
    inflation_label = 'Inflação'
    inflation_option_label = 'Taxa + Inflação (ex: 1% + IPCA)'
    inflation_yield = 'Taxa + Inflação (ex: 1% + IPCA)'
    invalid_bond_type_message = 'Tipo de rendimento inválido'
    liquid_yield_title = '<p><h3><center>Rendimento Líquido: {liquid_yield}%*</p> <p>*Com o resgate em {maturity_in_days} dias</p></center></h3>'
    main_title = f'<h1><center>Comparador de Renda Fixa</center></h1>'
    maturity_date_label = 'Data de Vencimento'
    maturity_in_days = 'Prazo de Vencimento (em dias)'
    maturity_hold_label = 'Informe o tempo que pretende manter o produto (em dias)'
    maturity_label = 'Informe a data de vencimento'
    not_hold_to_maturity = 'Não'
    post_fixed_option_label = 'Taxa Pós-fixada (em porcentagem; ex: 90% do CDI)'
    pre_fixed_option_label = 'Taxa Pré-fixada (ex: 10% a.a.)'
    poupanca_label = 'Poupança'
    product_label = 'Selecione seu produto'
    result_title = f'<h2><center>Comparativo do Seu Produto</center></h2>'
    retain_to_maturity_label = 'Você pretende manter até o vencimento?'
    selic_label = 'Selic'
    selic_option_label = 'Taxa + Selic (ex: 1% + Selic)'
    unknown_maturity = 'Não sei'
    yield_title = 'Selecione o tipo de rendimento'


class Menu:
    columns_qty = 2
    inflation_index_options = [
        InflationTypes.IPC,
        InflationTypes.IPCA,
        InflationTypes.IGPM
    ]
    maturity_options = [
        Text.unknown_maturity,
        Text.maturity_date_label,
        Text.maturity_in_days
    ]
    product_options = [
        'CDB',
        'Debênture',
        Text.credit_letters_label,
        'Tesouro Direto',
        Text.poupanca_label,
        'Caixinha Nubank'
    ]
    retain_to_maturity_options = [
        'Sim',
        Text.not_hold_to_maturity
    ]
    yield_options = [
        Text.pre_fixed_option_label,
        Text.post_fixed_option_label,
        Text.cdi_option_label,
        Text.selic_option_label,
        Text.inflation_option_label
    ]

class Settings:
    ALLOW_HTML = True
    METRIC_BORDER = True
