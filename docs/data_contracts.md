# Contratos de Dados

## Objetivo

Este documento descreve os contratos de dados do projeto `projeto_api_dados_abertos_camara`.

O objetivo é registrar, de forma clara, as expectativas mínimas de estrutura, qualidade e integridade para as principais tabelas produzidas pelo pipeline.

Os contratos de dados ajudam a garantir que as tabelas geradas nas camadas Bronze, Silver, Gold, Star Schema e Serving estejam consistentes, rastreáveis e adequadas para consumo analítico.

---

## Contexto

O projeto processa dados públicos da Câmara dos Deputados a partir de múltiplos endpoints da API. Esses dados passam por etapas de ingestão, limpeza, enriquecimento, modelagem dimensional e publicação para Power BI.

Como cada camada depende da anterior, é importante documentar o que cada tabela deve conter para ser considerada válida.

Os contratos de dados funcionam como uma ponte entre:

- modelagem de dados;
- Data Quality;
- documentação técnica;
- rastreabilidade;
- consumo analítico.

---

## Escopo

Este documento cobre:

- conceito de contrato de dados;
- objetivos dos contratos;
- convenção geral utilizada;
- regras gerais por camada;
- contratos por entidade;
- severidade das regras;
- exemplo de contrato declarativo;
- integração com Data Quality;
- boas práticas;
- próximas evoluções.

Este documento não substitui os schemas físicos finais das tabelas Delta. Ele funciona como documentação funcional e técnica das expectativas de dados.

---

## Conteúdo Principal

### 1. O que é um contrato de dados

Um contrato de dados define regras mínimas que uma tabela deve atender para ser considerada válida.

No contexto deste projeto, um contrato pode incluir:

- nome da tabela;
- camada do pipeline;
- origem dos dados;
- chave primária ou chave de negócio;
- grão da tabela;
- colunas obrigatórias;
- regras de nulidade;
- regras de unicidade;
- domínios permitidos;
- dependências com outras tabelas;
- validações de qualidade aplicáveis.

### 2. Objetivos dos contratos

Os contratos de dados têm como objetivos:

- documentar expectativas sobre cada tabela;
- apoiar validações automatizadas de Data Quality;
- facilitar manutenção e evolução do pipeline;
- reduzir risco de quebra entre camadas;
- aumentar a confiabilidade das tabelas consumidas no Power BI;
- melhorar rastreabilidade entre ingestão, transformação e Serving;
- apoiar revisão técnica do projeto.

### 3. Convenção geral

Cada contrato segue a estrutura abaixo:

```text
Tabela: nome_da_tabela
Camada: Bronze | Silver | Gold | Star | Serving
Origem: tabela ou endpoint de origem
Grão: nível de detalhe da tabela
Chave: chave primária, chave substituta ou chave de negócio
Colunas obrigatórias: campos mínimos esperados
Regras críticas: validações que devem bloquear a publicação
Regras de alerta: validações que geram aviso, mas não necessariamente bloqueiam o pipeline
```

### 4. Regras gerais por camada

#### 4.1 Bronze

A camada Bronze preserva os dados brutos da API com metadados técnicos.

Regras gerais:

- a tabela não deve estar vazia após ingestão bem-sucedida;
- deve conter identificadores da entidade quando disponíveis;
- deve preservar campos relevantes retornados pela API;
- deve incluir metadados de ingestão, quando aplicável;
- não deve aplicar regras analíticas complexas.

Validações recomendadas:

| Validação | Severidade | Descrição |
|---|---|---|
| `not_empty` | error | A tabela deve possuir registros. |
| `required_columns` | error | Colunas mínimas da entidade devem existir. |
| `no_nulls` | warning | Chaves principais não devem ser nulas quando fornecidas pela API. |

#### 4.2 Silver

A camada Silver padroniza, limpa e tipa os dados da Bronze.

Regras gerais:

- nomes de colunas devem estar padronizados;
- tipos de dados devem estar coerentes;
- datas devem estar convertidas;
- identificadores devem estar normalizados;
- duplicidades críticas devem ser removidas ou controladas.

Validações recomendadas:

| Validação | Severidade | Descrição |
|---|---|---|
| `required_columns` | error | Colunas padronizadas devem existir. |
| `no_nulls` | error | Chaves críticas não devem ser nulas. |
| `unique_key` | error | Chaves únicas devem permanecer únicas. |
| `max_null_ratio` | warning | Campos analíticos não devem exceder limite de nulos. |

#### 4.3 Gold

A camada Gold adiciona enriquecimentos analíticos, regras de negócio e classificações.

Regras gerais:

- deve manter rastreabilidade com a Silver;
- deve conter atributos derivados esperados;
- classificações devem ter origem identificada;
- fallbacks devem ser explícitos;
- campos analíticos críticos devem estar preenchidos quando possível.

Validações recomendadas:

| Validação | Severidade | Descrição |
|---|---|---|
| `required_columns` | error | Campos enriquecidos obrigatórios devem existir. |
| `no_nulls` | warning | Campos classificados devem ser preenchidos ou receber fallback. |
| `allowed_values` | warning | Categorias devem pertencer a domínios previstos. |
| `max_null_ratio` | warning | Taxa de nulos deve ficar dentro do limite definido. |

#### 4.4 Star Schema

A camada Star organiza os dados em dimensões e fatos.

Regras gerais:

- dimensões devem ser criadas antes dos fatos;
- fatos devem possuir grão bem definido;
- chaves substitutas devem ser geradas;
- relacionamentos entre fatos e dimensões devem ser consistentes;
- tabelas fato devem estar prontas para consumo analítico.

Validações recomendadas:

| Validação | Severidade | Descrição |
|---|---|---|
| `not_empty` | error | Dimensões e fatos não devem estar vazios. |
| `required_columns` | error | Chaves e atributos mínimos devem existir. |
| `unique_key` | error | Chaves de dimensão devem ser únicas. |
| `referential_integrity` | warning | Chaves dos fatos devem ter correspondência nas dimensões. |

#### 4.5 Serving

A camada Serving publica as tabelas finais para consumo analítico.

Regras gerais:

- somente tabelas aprovadas devem ser publicadas;
- nomes devem estar padronizados;
- schema final deve ser estável para o Power BI;
- tabelas devem estar acessíveis para consulta SQL;
- falhas críticas de qualidade devem impedir publicação.

Validações recomendadas:

| Validação | Severidade | Descrição |
|---|---|---|
| `not_empty` | error | Tabelas finais não devem estar vazias. |
| `required_columns` | error | Campos esperados pelo BI devem existir. |
| `schema_stability` | warning | Mudanças de schema devem ser controladas. |

### 5. Contratos por entidade

Os contratos abaixo representam uma documentação funcional das principais entidades do projeto. Os nomes podem ser ajustados conforme os nomes finais definidos nos registries e nas tabelas Delta.

#### 5.1 Deputados

##### Bronze — `deputados`

| Item | Regra |
|---|---|
| Camada | Bronze |
| Origem | Endpoint de deputados da API da Câmara. |
| Grão | Um registro por deputado retornado pela API. |
| Chave esperada | `id` ou identificador equivalente do deputado. |

Colunas obrigatórias recomendadas:

- `id`;
- `nome`;
- `siglaPartido` ou campo equivalente;
- `siglaUf` ou campo equivalente.

Regras críticas:

- tabela não vazia;
- coluna de identificador deve existir;
- identificador do deputado não deve ser nulo.

##### Silver — `deputados`

| Item | Regra |
|---|---|
| Camada | Silver |
| Origem | Bronze `deputados`. |
| Grão | Um registro padronizado por deputado. |
| Chave esperada | `id_deputado`. |

Colunas obrigatórias recomendadas:

- `id_deputado`;
- `nome_deputado`;
- `sigla_partido`;
- `sigla_uf`.

Regras críticas:

- `id_deputado` não nulo;
- `id_deputado` único;
- tipos de dados padronizados.

##### Star — `dim_deputado`

| Item | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold/Silver deputados. |
| Grão | Um registro por deputado na dimensão. |
| Chave substituta | `sk_deputado`. |
| Chave de negócio | `id_deputado`. |

Colunas obrigatórias recomendadas:

- `sk_deputado`;
- `id_deputado`;
- `nome_deputado`;
- `sigla_partido`;
- `sigla_uf`.

Regras críticas:

- `sk_deputado` não nulo;
- `id_deputado` não nulo;
- `sk_deputado` único;
- `id_deputado` único dentro da dimensão.

#### 5.2 Partidos

##### Silver — `partidos`

| Item | Regra |
|---|---|
| Camada | Silver |
| Origem | Bronze `partidos`. |
| Grão | Um registro por partido. |
| Chave esperada | `id_partido` ou `sigla_partido`. |

Colunas obrigatórias recomendadas:

- `id_partido`;
- `sigla_partido`;
- `nome_partido`.

Regras críticas:

- tabela não vazia;
- `sigla_partido` não nula;
- duplicidades devem ser controladas.

##### Star — `dim_partido`

| Item | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Silver/Gold partidos. |
| Grão | Um registro por partido. |
| Chave substituta | `sk_partido`. |
| Chave de negócio | `id_partido` ou `sigla_partido`. |

Colunas obrigatórias recomendadas:

- `sk_partido`;
- `id_partido`;
- `sigla_partido`;
- `nome_partido`.

Regras críticas:

- `sk_partido` único;
- `sigla_partido` não nula;
- domínio de siglas deve ser consistente.

#### 5.3 Proposições

##### Bronze — `proposicoes`

| Item | Regra |
|---|---|
| Camada | Bronze |
| Origem | Endpoint de proposições da API da Câmara. |
| Grão | Um registro por proposição retornada pela API. |
| Chave esperada | `id` ou identificador equivalente da proposição. |

Colunas obrigatórias recomendadas:

- `id`;
- `siglaTipo`;
- `numero`;
- `ano`;
- `ementa`;
- `dataApresentacao`.

Regras críticas:

- tabela não vazia;
- identificador da proposição não nulo;
- campos mínimos de identificação legislativa devem existir.

##### Silver — `proposicoes`

| Item | Regra |
|---|---|
| Camada | Silver |
| Origem | Bronze `proposicoes`. |
| Grão | Um registro padronizado por proposição. |
| Chave esperada | `id_proposicao`. |

Colunas obrigatórias recomendadas:

- `id_proposicao`;
- `sigla_tipo`;
- `numero`;
- `ano`;
- `ementa`;
- `data_apresentacao`.

Regras críticas:

- `id_proposicao` não nulo;
- `id_proposicao` único;
- `data_apresentacao` convertida para tipo de data ou timestamp;
- textos relevantes normalizados quando aplicável.

##### Gold — `proposicoes`

| Item | Regra |
|---|---|
| Camada | Gold |
| Origem | Silver `proposicoes` + regras/ML. |
| Grão | Um registro enriquecido por proposição. |
| Chave esperada | `id_proposicao`. |

Colunas obrigatórias recomendadas:

- `id_proposicao`;
- `sigla_tipo`;
- `numero`;
- `ano`;
- `ementa`;
- `data_apresentacao`;
- `tema_ementa`;
- `origem_tema`;
- `natureza_juridica`;
- `origem_natureza_juridica`;
- `tipo_documental`.

Regras críticas:

- `id_proposicao` não nulo;
- `id_proposicao` único;
- campos de classificação devem existir;
- origem da classificação deve ser preenchida;
- quando não houver classificação confiável, deve existir fallback explícito.

Domínios recomendados:

- `origem_tema`: `REGRA`, `ML`, `FALLBACK`, ou valores equivalentes usados no projeto;
- `origem_natureza_juridica`: `REGRA`, `ML`, `FALLBACK`, ou valores equivalentes usados no projeto.

##### Star — `dim_proposicao`

| Item | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `proposicoes`. |
| Grão | Um registro por proposição. |
| Chave substituta | `sk_proposicao`. |
| Chave de negócio | `id_proposicao`. |

Colunas obrigatórias recomendadas:

- `sk_proposicao`;
- `id_proposicao`;
- `sigla_tipo`;
- `numero`;
- `ano`;
- `ementa`;
- `tema_ementa`;
- `natureza_juridica`;
- `tipo_documental`.

Regras críticas:

- `sk_proposicao` único;
- `id_proposicao` único;
- campos descritivos essenciais devem existir.

##### Star — `fato_proposicao`

| Item | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `proposicoes` + dimensões relacionadas. |
| Grão | Uma linha por proposição. |
| Chave de fato | `id_proposicao` ou chave substituta equivalente. |

Colunas obrigatórias recomendadas:

- `sk_proposicao`;
- `sk_tempo`;
- `id_proposicao`;
- métricas e flags analíticas definidas no projeto.

Regras críticas:

- tabela não vazia;
- `sk_proposicao` não nula;
- relacionamento com `dim_proposicao` deve ser válido;
- relacionamento com `dim_tempo` deve ser válido quando houver data de apresentação.

#### 5.4 Demais entidades

Além de deputados, partidos e proposições, o projeto possui contratos recomendados para:

- autores de proposições;
- tramitações;
- votações;
- votos;
- órgãos;
- eventos;
- presença em eventos;
- tempo.

Resumo das regras esperadas:

| Entidade | Grão esperado | Regras principais |
|---|---|---|
| `proposicoes_autores` / `fato_autoria` | Uma linha por relação autor-proposição. | `id_proposicao` não nulo, autor identificado, duplicidades controladas. |
| `tramitacoes` / `fato_tramitacao` | Uma linha por movimentação de proposição. | `id_proposicao` não nulo, data/descrição preenchida, grão preservado. |
| `votacoes` / `fato_votacao` | Uma linha por votação. | `id_votacao` não nulo, votação única, data ou descrição presente. |
| `votos` / `fato_voto` | Uma linha por voto parlamentar. | `id_votacao` não nulo, parlamentar identificado, domínio de voto controlado. |
| `orgaos` / `dim_orgao` | Uma linha por órgão. | órgão identificado, chave ou sigla preenchida, duplicidades controladas. |
| `eventos` / `fato_evento` | Uma linha por evento legislativo. | `id_evento` não nulo, evento único, data ou descrição presente. |
| `presencas_eventos` / `fato_presenca` | Uma linha por presença parlamentar em evento. | `id_evento` não nulo, parlamentar identificado, duplicidades controladas. |
| `dim_tempo` | Uma linha por data. | `sk_tempo` único, `data` única, calendário cobrindo fatos. |

### 6. Severidade das regras

As regras podem ser classificadas em dois níveis principais.

#### Error

Regras do tipo `error` devem bloquear a continuação do pipeline ou impedir a publicação da tabela na camada Serving.

Exemplos:

- tabela vazia em etapa crítica;
- ausência de coluna obrigatória;
- chave primária nula;
- duplicidade em chave que deveria ser única;
- schema incompatível com a camada de consumo.

#### Warning

Regras do tipo `warning` não necessariamente bloqueiam o pipeline, mas devem gerar alerta e ser monitoradas.

Exemplos:

- percentual elevado de nulos em campo não crítico;
- categoria fora do domínio esperado;
- relacionamento ausente em pequena parcela dos registros;
- volume processado muito diferente da execução anterior.

### 7. Exemplo de contrato em formato declarativo

Abaixo está um exemplo conceitual de como um contrato poderia ser representado em configuração Python ou YAML.

```yaml
table: gold.proposicoes
layer: gold
grain: one row per proposition
primary_key: id_proposicao
required_columns:
  - id_proposicao
  - sigla_tipo
  - numero
  - ano
  - ementa
  - data_apresentacao
  - tema_ementa
  - origem_tema
  - natureza_juridica
  - origem_natureza_juridica
checks:
  - name: not_empty
    severity: error
  - name: no_nulls
    columns:
      - id_proposicao
    severity: error
  - name: unique_key
    columns:
      - id_proposicao
    severity: error
  - name: allowed_values
    column: origem_tema
    values:
      - REGRA
      - ML
      - FALLBACK
    severity: warning
```

### 8. Integração com Data Quality

Os contratos documentados aqui devem orientar a camada de Data Quality do projeto.

Relação esperada:

```text
Contrato de dados
      ↓
Regras declarativas
      ↓
Validações automatizadas
      ↓
Resultado da validação
      ↓
Decisão: bloquear, alertar ou publicar
```

Fluxo recomendado:

```text
1. Ler tabela produzida pela camada
2. Identificar contrato aplicável
3. Executar validações obrigatórias
4. Registrar resultado das validações
5. Bloquear avanço se houver erro crítico
6. Permitir avanço com alerta se houver apenas warnings
```

### 9. Boas práticas recomendadas

Para manter os contratos úteis e atualizados:

- atualizar este documento sempre que uma tabela mudar de schema;
- versionar mudanças relevantes de contrato;
- diferenciar regras críticas de regras de alerta;
- evitar regras excessivamente rígidas em campos naturalmente incompletos na API;
- priorizar chaves, colunas obrigatórias e integridade entre camadas;
- registrar exceções conhecidas;
- manter alinhamento entre contratos, código e documentação do Star Schema.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para os contratos de dados do projeto.

Ele se conecta diretamente a:

- `README.md`, que apresenta Data Contracts como competência demonstrada;
- `docs/architecture.md`, que posiciona contratos e qualidade dentro da arquitetura;
- `docs/data_quality.md`, que executa validações baseadas nos contratos;
- `docs/star_schema.md`, que define dimensões e fatos que precisam de integridade;
- `docs/execution_guide.md`, que recomenda validações por etapa;
- `docs/dashboard.md`, que depende de tabelas finais confiáveis;
- `docs/project_evolution.md`, que propõe contratos executáveis como evolução.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Qualidade de Dados](data_quality.md)
- [Modelo Star Schema](star_schema.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Linhagem dos Dados](lineage.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções dos contratos de dados:

- transformar contratos em arquivos YAML executáveis;
- criar um registry formal de contratos por tabela;
- integrar contratos ao runner de cada camada;
- persistir resultados das validações em tabela Delta;
- criar dashboard operacional de qualidade de dados;
- aplicar bloqueio automático antes da camada Serving;
- adicionar validação de integridade referencial entre fatos e dimensões;
- alinhar contratos com schemas físicos finais das tabelas Delta;
- versionar contratos por release do projeto.
