# Guia de Execução do Projeto

## Objetivo

Este documento apresenta o passo a passo recomendado para executar o pipeline do projeto `projeto_api_dados_abertos_camara`.

O objetivo é orientar a execução completa do projeto, desde a ingestão dos dados públicos da Câmara dos Deputados até a publicação das tabelas analíticas para consumo no Power BI.

Fluxo principal:

```text
Bronze → Silver → ML → Gold → Star Schema → Serving
```

---

## Contexto

O projeto foi desenvolvido com uma arquitetura lakehouse em camadas. Cada etapa do pipeline depende dos dados produzidos pela etapa anterior.

Por isso, a execução deve respeitar a ordem lógica das camadas:

1. Bronze;
2. Silver;
3. ML Training;
4. Gold;
5. Star Schema;
6. Serving;
7. Power BI.

A etapa de ML é executada antes da Gold porque os modelos treinados e registrados podem ser utilizados para enriquecer as proposições na camada Gold.

---

## Escopo

Este guia cobre:

- pré-requisitos de ambiente;
- configuração inicial;
- ordem geral de execução;
- execução das camadas Bronze, Silver, ML, Gold, Star Schema e Serving;
- validações recomendadas por etapa;
- checklist de execução completa;
- fluxo resumido;
- problemas comuns;
- conexão com os demais documentos da pasta `docs/`.

Este guia não substitui a documentação detalhada de arquitetura, contratos de dados, Star Schema, ML/NLP ou dashboard. Esses temas possuem documentos próprios.

---

## Conteúdo Principal

### 1. Pré-requisitos

Antes de executar o pipeline, confirme que o ambiente possui:

- Python configurado;
- dependências instaladas conforme `pyproject.toml`;
- PySpark disponível;
- Delta Lake configurado;
- acesso à internet para consumo da API pública da Câmara dos Deputados;
- variáveis de ambiente configuradas, quando aplicável;
- ambiente Databricks ou ambiente local compatível com Spark.

### 2. Configuração do ambiente

O projeto utiliza configurações centralizadas em `src/config/`.

Arquivos principais:

```text
src/config/
├── api_config.py
├── dataset_config.py
├── project_config.py
└── spark_config.py
```

Antes da execução, revise principalmente:

- `project_config.py`: caminhos de armazenamento, schemas e paths das camadas;
- `dataset_config.py`: datasets disponíveis, endpoints e dependências;
- `.env.example`: exemplo de variáveis de ambiente esperadas.

Quando executar localmente, crie um arquivo `.env` baseado no `.env.example`.

Exemplo:

```text
BASE_STORAGE_PATH=file:/tmp/dados_abertos_camara
```

### 3. Ordem geral de execução

A ordem recomendada é:

```text
1. Bronze
2. Silver
3. ML Training
4. Gold
5. Star Schema
6. Serving
7. Power BI
```

Essa ordem deve ser respeitada porque cada camada depende dos dados produzidos pela camada anterior.

### 4. Etapa Bronze — Ingestão dos dados brutos

#### Objetivo

A camada Bronze é responsável por consumir os dados da API pública da Câmara dos Deputados e armazená-los em formato Delta, preservando os dados o mais próximo possível da origem.

#### Entrada

Fonte externa:

```text
API Dados Abertos Câmara dos Deputados
```

#### Saída

Tabelas ou arquivos Delta na camada Bronze.

#### Execução

Execute o runner da camada Bronze:

```bash
python -m src.bronze.orchestration.runner
```

ou, no Databricks, execute o notebook ou comando equivalente que chama:

```text
src/bronze/orchestration/runner.py
```

#### Resultado esperado

Ao final da execução, devem ser gerados dados brutos para entidades como:

- deputados;
- partidos;
- órgãos;
- proposições;
- autores;
- tramitações;
- votações;
- votos;
- eventos;
- presença em eventos.

#### Validação recomendada

Após a Bronze, verifique:

- se os dados foram gravados no path correto;
- se os principais datasets possuem registros;
- se não houve falha de conexão com a API;
- se os logs indicam sucesso na ingestão.

### 5. Etapa Silver — Padronização e limpeza

#### Objetivo

A camada Silver transforma os dados brutos em dados padronizados, tipados e mais consistentes.

#### Entrada

Dados da camada Bronze.

#### Saída

Tabelas Delta na camada Silver.

#### Execução

Execute o runner da camada Silver:

```bash
python -m src.silver.orchestration.runner
```

ou, no Databricks:

```text
src/silver/orchestration/runner.py
```

#### Principais transformações

Nesta etapa podem ocorrer:

- renomeação de colunas;
- conversão de tipos;
- padronização de datas;
- normalização de textos;
- tratamento de nulos;
- remoção de duplicidades;
- padronização de identificadores.

#### Validação recomendada

Após a Silver, verifique:

- se as tabelas foram criadas corretamente;
- se as colunas obrigatórias existem;
- se as chaves principais estão preenchidas;
- se os tipos de dados estão coerentes;
- se as validações de qualidade foram executadas.

### 6. Etapa ML — Treinamento e registro dos classificadores

#### Objetivo

A etapa de Machine Learning prepara e registra os modelos utilizados para classificação textual de proposições.

O projeto utiliza classificação para enriquecer os dados com informações como:

- tema da proposição;
- natureza jurídica;
- origem da classificação.

#### Entrada

Dados tratados, regras, dicionários e bases de treinamento do módulo `src/ml/`.

#### Saída

Modelos treinados e registrados para uso posterior na camada Gold.

#### Execução

Execute o runner de treinamento:

```bash
python -m src.ml.orchestration.training_runner
```

ou o ponto de entrada principal do módulo de ML, quando aplicável:

```bash
python -m src.ml.main
```

#### Resultado esperado

Ao final da execução, espera-se que os classificadores estejam treinados e disponíveis para inferência.

No ambiente Databricks/MLflow, confirme se os modelos foram registrados corretamente e se o alias esperado está disponível, por exemplo:

```text
champion
```

#### Validação recomendada

Após o treinamento, verifique:

- se o modelo foi registrado;
- se o alias do modelo está correto;
- se a inferência de teste retorna classificações válidas;
- se há fallback configurado para textos sem classificação confiável.

### 7. Etapa Gold — Enriquecimento analítico

#### Objetivo

A camada Gold adiciona regras de negócio, atributos derivados e classificações aos dados padronizados.

#### Entrada

Dados da camada Silver e modelos/regras do módulo ML.

#### Saída

Tabelas Delta enriquecidas na camada Gold.

#### Execução

Execute o runner da camada Gold:

```bash
python -m src.gold.orchestration.runner
```

ou, no Databricks:

```text
src/gold/orchestration/runner.py
```

#### Principais enriquecimentos

Nesta etapa podem ser gerados campos como:

- tema da proposição;
- origem do tema;
- natureza jurídica;
- origem da natureza jurídica;
- tipo documental;
- categoria regimental;
- flags analíticas;
- classificações derivadas de textos legislativos.

#### Validação recomendada

Após a Gold, verifique:

- se as classificações foram aplicadas;
- se os campos derivados foram criados;
- se os registros mantêm rastreabilidade com a Silver;
- se não houve erro na chamada dos modelos ML;
- se os fallbacks foram aplicados quando necessário.

### 8. Etapa Star Schema — Modelo dimensional

#### Objetivo

A etapa Star Schema organiza os dados enriquecidos em um modelo dimensional para análise.

Essa camada estrutura os dados em:

- dimensões;
- fatos;
- chaves substitutas;
- tabelas analíticas integradas.

#### Entrada

Dados da camada Gold.

#### Saída

Tabelas dimensionais e fatos na camada Star.

#### Execução

Execute o runner da camada Star:

```bash
python -m src.star.orchestration.runner
```

ou, no Databricks:

```text
src/star/orchestration/runner.py
```

#### Ordem interna recomendada

A ordem conceitual esperada é:

```text
1. Dimensões
2. Fatos
```

As dimensões devem ser criadas antes das tabelas fato, pois os fatos dependem das chaves dimensionais.

#### Exemplos de tabelas esperadas

Dimensões:

- dimensão de deputados;
- dimensão de partidos;
- dimensão de proposições;
- dimensão de temas;
- dimensão de tempo;
- dimensão de órgãos.

Fatos:

- fato de proposições;
- fato de votações;
- fato de votos;
- fato de presença;
- fato de eventos.

#### Validação recomendada

Após a Star, verifique:

- se as dimensões foram criadas antes dos fatos;
- se as chaves substitutas foram geradas;
- se os joins entre fatos e dimensões estão corretos;
- se não há perda indevida de registros;
- se as tabelas fato estão prontas para consumo analítico.

### 9. Etapa Serving — Publicação das tabelas finais

#### Objetivo

A camada Serving publica as tabelas finais para consumo analítico, principalmente pelo Power BI.

#### Entrada

Tabelas da camada Star Schema.

#### Saída

Tabelas finais publicadas em schema ou local de consumo.

#### Execução

Execute o processo de publicação da camada Serving:

```bash
python -m src.serving.publish_tables
```

ou, no Databricks, execute o notebook/script equivalente em:

```text
src/serving/
```

#### Resultado esperado

Ao final, as tabelas finais devem estar disponíveis para conexão no Power BI ou outra ferramenta analítica.

#### Validação recomendada

Após o Serving, verifique:

- se as tabelas foram publicadas no schema correto;
- se o Power BI consegue acessar as tabelas;
- se os nomes das tabelas estão padronizados;
- se as medidas e visuais esperados conseguem ser construídos.

### 10. Checklist de execução completa

Use este checklist para validar uma execução ponta a ponta:

```text
[ ] Configurar ambiente e variáveis
[ ] Instalar dependências
[ ] Executar Bronze
[ ] Validar ingestão Bronze
[ ] Executar Silver
[ ] Validar padronização Silver
[ ] Executar ML
[ ] Validar modelos e inferência
[ ] Executar Gold
[ ] Validar enriquecimentos e classificações
[ ] Executar Star Schema
[ ] Validar dimensões e fatos
[ ] Executar Serving
[ ] Validar publicação das tabelas finais
[ ] Atualizar ou validar dashboard Power BI
```

### 11. Fluxo resumido

```text
API Câmara
   ↓
Bronze
   ↓
Silver
   ↓
ML Training / ML Inference
   ↓
Gold
   ↓
Star Schema
   ↓
Serving
   ↓
Power BI
```

### 12. Problemas comuns

#### Falha ao ler variáveis de ambiente

Verifique se o arquivo `.env` existe e se foi criado com base no `.env.example`.

#### Erro de path de armazenamento

Confirme se `BASE_STORAGE_PATH` está configurado corretamente em ambiente local ou Databricks.

#### Tabelas Silver vazias

Verifique se a Bronze foi executada antes da Silver e se os endpoints da API retornaram dados.

#### Erro na inferência ML

Confirme se os modelos foram treinados, registrados e se o alias utilizado pelo projeto está disponível.

#### Fatos sem relacionamento com dimensões

Verifique se as dimensões foram geradas antes das tabelas fato e se as chaves de relacionamento estão corretas.

### 13. Observações para portfólio

Este guia documenta a execução lógica do pipeline e deve ser usado junto com os demais documentos da pasta `docs/`.

A execução completa demonstra conhecimentos em:

- ingestão de dados;
- arquitetura medalhão;
- PySpark;
- Delta Lake;
- Machine Learning aplicado a texto;
- modelagem dimensional;
- publicação para BI.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para execução do pipeline.

Ele se conecta diretamente a:

- `README.md`, que apresenta o comando resumido de execução;
- `docs/architecture.md`, que explica a arquitetura e a ordem das camadas;
- `docs/data_quality.md`, que documenta validações aplicadas ao pipeline;
- `docs/data_contracts.md`, que define regras esperadas para as tabelas;
- `docs/ml_nlp.md`, que explica o módulo de classificação textual;
- `docs/star_schema.md`, que detalha dimensões e fatos;
- `docs/dashboard.md`, que documenta o consumo final no Power BI.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Qualidade de Dados](data_quality.md)
- [Contratos de Dados](data_contracts.md)
- [Classificação ML/NLP](ml_nlp.md)
- [Modelo Star Schema](star_schema.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções para a execução do projeto:

- transformar a execução sequencial em workflow orquestrado;
- criar jobs no Databricks Workflows;
- configurar retries e alertas;
- criar CI/CD com GitHub Actions;
- adicionar validação automática antes da execução da próxima camada;
- persistir logs de execução em tabela Delta;
- documentar parâmetros de execução por ambiente;
- criar modo de execução parcial por dataset ou camada;
- adicionar troubleshooting mais detalhado por erro conhecido.
