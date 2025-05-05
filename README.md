```python
# executando app
streamlit run src/main.py  
```

## Regras de negócio:
- `data de vencimento`: recebe uma data no formato `DD-MM-YYYY` ou prazo em dias
  - Com o valor 'Não sei', o valor padrão é 360 dias
  - O cálculo comparativo é feito comparando a data da consulta
  - O cálculo descapitaliza o vencimento em dias para o comparativo
