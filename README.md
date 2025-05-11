# Boas vindas ao **Comparador de Renda Fixa**!

Este projeto é uma aplicação em **Streamlit** que permite comparar diferentes produtos de investimento de renda fixa, como **CDBs**, **LCIs**, **LCAs** e **Tesouro Direto**, com base em **taxas atuais de mercado** e **parâmetros personalizados**.

## Link da aplicação:
<a href="https://comparador-renda-fixa.streamlit.app/" target="_blank">https://comparador-renda-fixa.streamlit.app/</a>

# <a id='topicos'>Tópicos</a>
- [Executando projeto](#executing)
- [Arquitetura do projeto](#arch)
  - [Padrões de projeto utilizados](#patterns)
  - [Otimização](#optimization)
- [Regras de negócio](#rules)
  - [Tipos de rendimento](#types)
  - [Vencimento](#maturity)
  - [Manter até vencimento](#hold)
  - [Métricas de comparação](#metrics)
- [Visão do app](#app)
- [Próximos passos](#next)

## <a id='executing'>[Executando o Projeto](#topicos)</a>

> **IMPORTANTE: Todos os cenários consideram a execução do projeto à partir do seu diretório raiz.
<br/> Logo após cloná-lo abra a pasta resultado em seu terminal**

Para iniciar a aplicação localmente:

```bash
# no diretório gerado com o clone do projeto: 
# instale as dependências:
pip install --no-cache-dir -r requirements.txt

# inicie a aplicação
streamlit run src/main.py

# ou via docker, construa a imagem localmente:
docker build -t comparador_renda_fixa . 

# execute a imagem:
docker run -p 8501:8501 comparador_renda_fixa
```
* Acesse a aplicação em:
<a href="http://localhost:8501" target="_blank">http://localhost:8501</a>

## <a id='arch'>[Arquitetura do projeto](#topicos)</a>

```bash
src/
├── configs/          # Configurações globais, enums e componentes textuais
├── controllers/      # Camada de controle (coordenadores entre view e domínio)
├── domain/           # Camada de lógica de negócios (uso de Facade para simplificação)
├── models/           # Estruturas de dados (entrada, saída, entidades)
├── services/         # Lógica aplicada, integração com dados e cálculos
└── views/            # Camada de visualização (elementos e renderizações Streamlit)
```
### <a id='patterns'>[Padrões de Projeto Utilizados](#topicos)</a>
* **Facade Pattern:** simplifica a orquestração entre serviços de rendimento e regras de negócio (`domain/yield_facade.py`).
* **Strategy Pattern:** versão simplifica, com cada tipo de rendimento (pré, pós, híbrido, IPCA, etc.) implementando uma estratégia diferente de cálculo, permitindo fácil expansão e manutenção da lógica (`services/yields.py`).
* **Enum + Mapeamentos:** padronização e internacionalização via YieldType e Text (`configs/yield_types.py, configs/components.py`).
* **Separação em camadas (MVC adaptado):** modelos de dados, lógica de negócio, visualização e controle desacoplados.

### <a id='optimization'>[Otimização](#topicos)</a>
* **Cache de Dados:** otimização via memorização para evitar múltiplas chamadas desnecessárias a APIs públicas de índices econômicos (uso de `@st.cache_data`).

## <a id='rules'>[Regras de Negócio](#topicos)</a>
### <a id='types'>[Tipos de rendimento](#topicos)</a>
* **Taxa Pré-fixada:** ex: 10% a.a.
* **Taxa Pós-fixada:** ex: 90%CDI a.a.
* **Taxa + CDI:** ex: 1% + CDI
* **Taxa + Selic:** ex: 1% + Selic
* **Taxa + Inflação:** ex: 1% + IPCA
### <a id='maturity'>[Vencimento](#topicos)</a>
* Pode ser informado como uma data (DD-MM-YYYY) ou como um prazo em dias
* Se informado como `"Não sei"`, o padrão será `360` dias
* Comparações são feitas com base na data atual da consulta
### <a id='hold'>[Manter até vencimento](#topicos)</a>
* **Sim:** considera rendimento completo até a data/prazo final
* **Não:** calcula rendimento proporcional ao prazo informado
### <a id='metrics'>[Métricas de comparação](#topicos)</a>
* **CDI:** taxa CDI diária anualizada (base 252)
* **Selic:** meta Selic atual
* **Inflação:** índice acumulado em 12 meses
  * Se o título não for atrelado à inflação, assume-se IPCA como padrão para comparação
* **Taxa Líquida:** considera a taxa real líquida do investimento
* **Letras de Crédito (LCI/LCA)**
  * Não sofrem tributação
  * Na comparação com outras medidas, é aplicada uma equivalência líquida, com base no imposto aplicável para outros títulos no mesmo prazo
    * `ex: taxa_equivalente(13%,100 dias) = (1,13)x(1+0,225)`

## <a id='app'>[Visão do app](#topicos)</a>
No seu servidor local, na porta 8501, ou no link, a aplicação deve ficar disponível, como abaixo:

![comparador gif](docs/app.gif)

No arquivo [mvp/main.py](mvp/main.py) é possível consultar a versão MVP do app.

## <a id='next'>[Próximos Passos](#topicos)</a>
### Refatoração de Controllers e Views
* Estilização da interface gráfica
* Maior responsabilidade única por classe
* Desacoplamento com inversão de dependências

### Funcionalidades Premium
* Login com persistência de histórico
* Comparações avançadas com séries temporais
* Sugestões automáticas de produtos equivalentes
* Seção de educação financeira, com base de cálculo explicada

### Ciclo de Integração Contínua
* Testes automatizados
* Pipeline de versionamento e deploy
* Hospedagem contínua da aplicação (clouds)
