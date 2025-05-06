```python
# executando app
streamlit run src/main.py  
```

## Regras de negócio:
- tipo de rendimento:
  - Taxa Pré-fixada (ex: 10% a.a.)
  - Taxa + CDI (ex: 1% + CDI)
  - Taxa + Selic (ex: 1% + Selic)
  - Taxa + Inflação (ex: 1% + IPCA)
- `data de vencimento`: recebe uma data no formato `DD-MM-YYYY` ou prazo em dias
  - Com o valor 'Não sei', o valor padrão é 360 dias
  - O cálculo comparativo é feito comparando a data da consulta
  - O cálculo descapitaliza o vencimento em dias para o comparativo
- `mantem o título até o vencimento`: 
  - Sim: calcula o rendimento até o vencimento
  - Não: calcula o rendimento até a data informada
- `métrica de comparação`: 
  - CDI: taxa CDI atual
  - Selic: taxa Selic atual
  - IPCA: inflação acumulada em 12 meses.
    - Se título não for inflação, o padrão é IPCA
  - Taxa Líquida: taxa de rendimento líquida
