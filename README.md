# Pipeline Lakehouse de Dados Abertos da Câmara dos Deputados

Projeto completo de Engenharia de Dados para ingestão, tratamento, enriquecimento, classificação e modelagem analítica de dados públicos da Câmara dos Deputados.

O projeto transforma dados brutos da API pública da Câmara em um produto analítico estruturado, utilizando arquitetura medalhão, Delta Lake, PySpark, classificação híbrida com NLP/ML, modelo dimensional em star schema e camada de serving para consumo em Power BI.



## Visão Geral

Este projeto foi desenvolvido com o objetivo de simular um pipeline moderno de dados legislativos, cobrindo etapas essenciais de um fluxo real de Engenharia de Dados:

- ingestão de dados via API pública;
- armazenamento em Delta Lake;
- arquitetura medalhão com camadas Bronze, Silver e Gold;
- tratamento e padronização com PySpark;
- enriquecimento analítico dos dados;
- classificação temática e jurídica de proposições legislativas;
- uso de MLflow para rastreamento e versionamento de modelos;
- construção de modelo dimensional em star schema;
- publicação de tabelas analíticas para consumo em Power BI;
- logs estruturados e rastreabilidade de execução.

O domínio escolhido foi o legislativo brasileiro, com dados públicos disponibilizados pela Câmara dos Deputados.



## Problema de Negócio

Os dados legislativos públicos são ricos, mas estão distribuídos em múltiplos endpoints, possuem estruturas diferentes e exigem tratamento antes de serem usados em análises.

Este projeto organiza esses dados para responder perguntas como:

- Quais temas legislativos aparecem com maior frequência?
- Quais deputados e partidos estão mais associados às proposições?
- Como proposições tramitam ao longo do tempo?
- Como ocorrem votações e votos parlamentares?
- Quais órgãos participam dos eventos legislativos?
- Como transformar dados brutos da API em tabelas analíticas para BI?

A proposta é transformar dados públicos dispersos em uma base analítica confiável, organizada e pronta para exploração.



## Arquitetura do Projeto

O pipeline segue uma arquitetura lakehouse em camadas.

```text
API Dados Abertos Câmara
        ↓
Bronze - Ingestão bruta
        ↓
Silver - Padronização e limpeza
        ↓
Gold - Enriquecimento analítico e classificação
        ↓
ML/NLP - Classificação temática e jurídica
        ↓
Star Schema - Fatos e dimensões
        ↓
Serving SQL
        ↓
Power BI
```


## Arquitetura Medalhão

### Bronze

A camada Bronze é responsável pela ingestão dos dados brutos da API.

Principais características:

* ingestão de múltiplos endpoints;
* suporte a paginação;
* ingestão incremental;
* ingestão de endpoints dependentes;
* controle de watermark;
* persistência em Delta Lake;
* inclusão de metadados técnicos;
* logs de execução.

Exemplos de entidades ingeridas:

* deputados;
* partidos;
* órgãos;
* proposições;
* tramitações;
* autores;
* votações;
* votos;
* eventos;
* presença em eventos.



### Silver

A camada Silver é responsável pela padronização e limpeza dos dados.

Principais responsabilidades:

* normalização de nomes de colunas;
* conversão de tipos;
* tratamento de datas;
* tratamento de valores nulos;
* padronização textual;
* remoção de duplicidades;
* preparação dos dados para enriquecimento.

Essa camada transforma os dados brutos em dados confiáveis e consistentes para uso analítico.



### Gold

A camada Gold é responsável pelo enriquecimento analítico.

Principais responsabilidades:

* criação de atributos derivados;
* classificação de proposições;
* categorização de votos;
* enriquecimento de tramitações;
* criação de flags analíticas;
* preparação dos dados para modelagem dimensional.

Nesta camada também ocorre a integração com a lógica de classificação temática e jurídica.



### Star Schema

A camada Star transforma os dados enriquecidos em um modelo dimensional voltado para consumo analítico.

O objetivo é facilitar consultas, análises e construção de dashboards no Power BI.



## Tecnologias Utilizadas

| Categoria                 | Tecnologia                             |
| - | -- |
| Linguagem                 | Python                                 |
| Processamento distribuído | PySpark                                |
| Armazenamento             | Delta Lake                             |
| Arquitetura               | Medallion Architecture                 |
| Modelagem analítica       | Star Schema                            |
| Machine Learning          | scikit-learn                           |
| NLP                       | TF-IDF, Regex, classificação textual   |
| MLOps                     | MLflow                                 |
| BI                        | Power BI                               |
| Observabilidade           | Logs estruturados                      |
| Fonte de dados            | API Dados Abertos Câmara dos Deputados |



## Estrutura de Pastas

```text
src/
  bronze/
    ingest/
    orchestration/
    monitoring/

  silver/
    transforms/
    registry/
    orchestration/

  gold/
    transforms/
    classification/
    registry/
    orchestration/

  star/
    dimensions/
    facts/
    registry/
    orchestration/

  ml/
    base/
    dictionaries/
    features/
    training/
    inference/
    orchestration/

  serving/

  config/

  utils/
    api/
    storage/
    monitoring/
    helpers/
```



## Organização do Código

O projeto foi organizado para separar responsabilidades por domínio técnico.

### `config/`

Contém configurações globais do projeto, como:

* endpoints da API;
* datasets disponíveis;
* caminhos de armazenamento;
* parâmetros de Spark;
* configurações de pipeline.

### `utils/`

Contém funções reutilizáveis para:

* chamadas de API;
* leitura e escrita Delta;
* logging;
* controle de watermark;
* geração de chaves;
* validações auxiliares.

### `bronze/`

Contém a lógica de ingestão dos dados brutos.

Inclui diferentes estratégias de ingestão:

* ingestão simples;
* ingestão incremental;
* ingestão de datasets dependentes.

### `silver/`

Contém transformações de limpeza e padronização.

### `gold/`

Contém enriquecimentos analíticos, classificações e regras de negócio.

### `ml/`

Contém os componentes de NLP e Machine Learning:

* pré-processamento textual;
* dicionários;
* extração de features;
* treinamento;
* inferência;
* registro de modelos.

### `star/`

Contém a construção das dimensões e fatos do modelo analítico.

### `serving/`

Contém a publicação das tabelas finais para consumo analítico.



## Fonte de Dados

A fonte principal é a API pública de Dados Abertos da Câmara dos Deputados.

Os dados utilizados incluem informações sobre:

* deputados;
* partidos;
* órgãos legislativos;
* proposições;
* autores de proposições;
* tramitações;
* votações;
* votos;
* eventos;
* presença em eventos.

A documentação oficial da API pode ser consultada no portal de Dados Abertos da Câmara dos Deputados.



## Pipeline de Ingestão

A ingestão foi desenhada para lidar com diferentes padrões de endpoints.

### Ingestão simples

Utilizada para entidades que podem ser extraídas diretamente da API.

Exemplos:

* deputados;
* partidos;
* órgãos.

### Ingestão incremental

Utilizada para datasets que possuem atualização periódica e podem ser filtrados por data.

Exemplos:

* proposições;
* eventos;
* votações.

### Ingestão dependente

Utilizada para endpoints que dependem de uma entidade pai.

Exemplos:

```text
/proposicoes/{id}/autores
/proposicoes/{id}/tramitacoes
/proposicoes/{id}/votacoes
/votacoes/{id}/votos
/eventos/{id}/deputados
```

Essa abordagem permite navegar por relações hierárquicas da API.



## Delta Lake

O projeto utiliza Delta Lake para armazenamento das tabelas nas camadas Bronze, Silver, Gold e Star.

Principais benefícios:

* persistência confiável;
* suporte a schema;
* possibilidade de upsert;
* histórico transacional;
* compatibilidade com arquitetura lakehouse;
* integração com Spark.

As operações de leitura, escrita e merge foram centralizadas em utilitários reutilizáveis.



## Observabilidade e Logs

O pipeline possui logs estruturados para rastrear execuções.

Os logs registram informações como:

* identificador da execução;
* camada do pipeline;
* nome do dataset;
* status da execução;
* mensagem;
* quantidade de registros;
* timestamp.

Essa abordagem facilita auditoria, rastreabilidade e investigação de falhas.

Exemplo conceitual de log:

```text
execution_id | layer  | dataset      | status  | records | timestamp
-|--|--|||-
abc123       | bronze | proposicoes  | success | 10000   | 2026-05-28 10:00
```



## Classificação NLP/ML

Um dos diferenciais do projeto é a classificação de proposições legislativas.

A solução utiliza uma estratégia híbrida:

1. **Regras regex**, para capturar padrões explícitos do texto legislativo;
2. **Dicionários temáticos**, para apoiar a classificação;
3. **Modelo supervisionado**, para generalizar padrões textuais;
4. **MLflow**, para rastrear experimentos e registrar modelos;
5. **Fallback**, para evitar classificações forçadas em textos ambíguos.



## Classificação Temática

A classificação temática busca identificar o principal tema de uma proposição legislativa.

Exemplos de temas possíveis:

* Saúde;
* Educação;
* Segurança Pública;
* Meio Ambiente;
* Economia;
* Direitos Humanos;
* Trabalho;
* Administração Pública;
* Tributação;
* Infraestrutura.

A classificação considera textos como ementa, descrição e demais campos relevantes.



## Classificação de Natureza Jurídica

Além do tema, o projeto também classifica a natureza da proposição.

Exemplos de categorias:

* criação de política pública;
* alteração normativa;
* revogação;
* autorização;
* concessão;
* homenagem;
* instituição de datas comemorativas;
* regulamentação.

Essa etapa ajuda a diferenciar o assunto da proposição de sua finalidade legislativa.



## MLflow

O MLflow é utilizado para apoiar o ciclo de vida dos modelos.

Principais usos:

* registro de experimentos;
* armazenamento de métricas;
* registro de parâmetros;
* versionamento de modelos;
* carregamento de modelos para inferência.

Essa abordagem aproxima o projeto de práticas de MLOps.



## Modelo Dimensional

O projeto cria um modelo em star schema para facilitar análises em ferramentas de BI.

### Dimensões

| Dimensão         | Descrição                                     |
| - | - |
| `dim_tempo`      | Calendário analítico para cruzamento temporal |
| `dim_deputado`   | Informações dos deputados                     |
| `dim_partido`    | Informações dos partidos                      |
| `dim_proposicao` | Informações principais das proposições        |
| `dim_evento`     | Informações dos eventos legislativos          |
| `dim_orgao`      | Informações dos órgãos da Câmara              |

### Fatos

| Fato              | Granularidade                         |
| -- | - |
| `fato_proposicao` | Uma linha por proposição              |
| `fato_autoria`    | Relação entre proposição e autor      |
| `fato_tramitacao` | Uma linha por movimentação/tramitação |
| `fato_votacao`    | Uma linha por votação                 |
| `fato_voto`       | Uma linha por voto parlamentar        |
| `fato_evento`     | Uma linha por evento                  |
| `fato_presenca`   | Uma linha por presença em evento      |



## Modelo Analítico

O modelo dimensional permite responder perguntas como:

* Quantas proposições foram apresentadas por ano?
* Quais temas legislativos são mais frequentes?
* Quais partidos têm mais proposições associadas?
* Quais deputados aparecem como autores?
* Como as proposições tramitam ao longo do tempo?
* Como os votos se distribuem por partido?
* Quais órgãos concentram mais eventos?
* Qual a participação dos deputados em eventos?



## Serving Analítico

A camada de serving publica as tabelas finais para consumo analítico.

Essa etapa prepara os dados para uso em:

* Power BI;
* consultas SQL;
* exploração analítica;
* painéis executivos;
* análises legislativas.



## Power BI

O projeto foi pensado para ser consumido em Power BI a partir das tabelas finais do star schema.

Sugestões de páginas para o dashboard:

### Visão Geral

* total de proposições;
* total de deputados;
* total de votações;
* total de eventos;
* evolução temporal.

### Proposições

* proposições por tema;
* proposições por tipo;
* proposições por ano;
* proposições por partido;
* principais autores.

### Votações

* votações por período;
* votos por partido;
* distribuição de votos;
* análise por proposição.

### Deputados

* autores mais frequentes;
* presença em eventos;
* participação em votações;
* distribuição por partido e UF.

### Eventos

* eventos por órgão;
* presença parlamentar;
* evolução temporal dos eventos.

## Data Quality

O projeto possui uma camada formal de Data Quality baseada em contratos declarativos por tabela e camada.

As validações incluem:

- dataset não vazio;
- colunas obrigatórias;
- chaves não nulas;
- unicidade de chaves;
- percentual máximo de nulos;
- domínio de valores permitidos.

As regras podem ser classificadas como `error`, quando bloqueiam o pipeline, ou `warning`, quando apenas registram alertas.

Os resultados podem ser persistidos em uma tabela Delta de monitoramento para auditoria e rastreabilidade.

## Como Executar

A execução depende do ambiente Spark/Databricks configurado.

Ordem conceitual de execução:

```bash
python -m src.bronze.orchestration.runner
python -m src.silver.orchestration.runner
python -m src.ml.orchestration.training_runner
python -m src.gold.orchestration.runner
python -m src.star.orchestration.runner
python -m src.serving.publish_tables
```

Em ambientes Databricks, os módulos podem ser executados como notebooks ou jobs, respeitando a ordem das camadas.



## Configuração

O projeto centraliza configurações em arquivos dentro de `src/config`.

Principais configurações:

* endpoints da API;
* datasets disponíveis;
* chaves primárias;
* dependências entre datasets;
* parâmetros incrementais;
* caminhos de armazenamento;
* schemas das camadas;
* configurações Spark.

Recomenda-se utilizar variáveis de ambiente para parametrizar caminhos e credenciais em ambientes produtivos.



## Exemplo de Fluxo

Exemplo simplificado do fluxo de proposições:

```text
1. Ingestão das proposições via API
2. Armazenamento bruto na Bronze
3. Padronização de campos na Silver
4. Classificação temática e jurídica na Gold
5. Criação de dimensão `dim_proposicao`
6. Criação de fatos relacionados
7. Publicação para consumo no Power BI
```



## Decisões Técnicas

### Por que arquitetura medalhão?

A arquitetura medalhão permite separar responsabilidades e aumentar a confiabilidade do pipeline.

* Bronze preserva o dado bruto;
* Silver cria uma versão limpa e padronizada;
* Gold adiciona valor analítico;
* Star organiza os dados para BI.

### Por que Delta Lake?

Delta Lake oferece recursos importantes para pipelines analíticos:

* transações ACID;
* schema enforcement;
* merge/upsert;
* histórico;
* melhor confiabilidade no data lake.

### Por que PySpark?

PySpark permite processar dados em escala e é amplamente usado em ambientes lakehouse e Databricks.

### Por que star schema?

O star schema facilita o consumo por ferramentas de BI, melhora a clareza analítica e organiza fatos e dimensões de forma intuitiva.

### Por que regex + ML?

No domínio legislativo, muitas categorias possuem padrões textuais explícitos. Regex captura bem esses padrões. O ML complementa a classificação ao generalizar textos menos diretos.


## Evoluções Futuras

* Criação CI/CD;
* Melhorar avaliação do modelo NLP;


## Fonte

Este projeto utiliza dados públicos disponibilizados pela Câmara dos Deputados.

[Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/swagger/api.html)
