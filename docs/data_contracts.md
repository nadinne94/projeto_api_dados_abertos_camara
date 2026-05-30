# Contratos de Dados

Este documento descreve os contratos de dados do projeto `projeto_api_dados_abertos_camara`.

O objetivo é registrar, de forma clara, quais são as expectativas mínimas de estrutura, qualidade e integridade para as principais tabelas produzidas pelo pipeline.

Os contratos de dados ajudam a garantir que as tabelas geradas nas camadas Bronze, Silver, Gold, Star Schema e Serving estejam consistentes, rastreáveis e adequadas para consumo analítico.

---

## 1. O que é um contrato de dados

Um contrato de dados define regras mínimas que uma tabela deve atender para ser considerada válida.

No contexto deste projeto, um contrato pode incluir:

- nome da tabela;
- camada do pipeline;
- origem dos dados;
- chave primária ou chave de negócio;
- colunas obrigatórias;
- regras de nulidade;
- regras de unicidade;
- domínios permitidos;
- dependências com outras tabelas;
- validações de qualidade aplicáveis.

---

## 2. Objetivos dos contratos

Os contratos de dados têm como objetivos:

- documentar expectativas sobre cada tabela;
- apoiar validações automatizadas de Data Quality;
- facilitar manutenção e evolução do pipeline;
- reduzir risco de quebra entre camadas;
- aumentar a confiabilidade das tabelas consumidas no Power BI;
- melhorar rastreabilidade entre ingestão, transformação e serving.

---

## 3. Convenção geral

Cada contrato segue a estrutura abaixo:

```text
Tabela: nome_da_tabela
Camada: Bronze | Silver | Gold | Star | Serving
Origem: tabela ou endpoint de origem
Grão: nível de detalhe da tabela
Chave: chave primária ou chave de negócio
Colunas obrigatórias: campos mínimos esperados
Regras críticas: validações que devem bloquear a publicação
Regras de alerta: validações que geram aviso, mas não necessariamente bloqueiam o pipeline
```

---

## 4. Regras gerais por camada

### 4.1 Bronze

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

---

### 4.2 Silver

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

---

### 4.3 Gold

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

---

### 4.4 Star Schema

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

---

### 4.5 Serving

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

---

# 5. Contratos por entidade

Os contratos abaixo representam uma documentação funcional das principais entidades do projeto. Os nomes podem ser ajustados conforme os nomes finais definidos nos registries e nas tabelas Delta.

---

## 5.1 Deputados

### Bronze — `deputados`

| Campo | Regra |
|---|---|
| Camada | Bronze |
| Origem | Endpoint de deputados da API da Câmara |
| Grão | Um registro por deputado retornado pela API |
| Chave esperada | `id` ou identificador equivalente do deputado |

Colunas obrigatórias recomendadas:

- `id`;
- `nome`;
- `siglaPartido` ou campo equivalente;
- `siglaUf` ou campo equivalente.

Regras críticas:

- tabela não vazia;
- coluna de identificador deve existir;
- identificador do deputado não deve ser nulo.

---

### Silver — `deputados`

| Campo | Regra |
|---|---|
| Camada | Silver |
| Origem | Bronze `deputados` |
| Grão | Um registro padronizado por deputado |
| Chave esperada | `id_deputado` |

Colunas obrigatórias recomendadas:

- `id_deputado`;
- `nome_deputado`;
- `sigla_partido`;
- `sigla_uf`.

Regras críticas:

- `id_deputado` não nulo;
- `id_deputado` único;
- tipos de dados padronizados.

---

### Star — `dim_deputado`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold/Silver deputados |
| Grão | Um registro por deputado na dimensão |
| Chave substituta | `sk_deputado` |
| Chave de negócio | `id_deputado` |

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

---

## 5.2 Partidos

### Silver — `partidos`

| Campo | Regra |
|---|---|
| Camada | Silver |
| Origem | Bronze `partidos` |
| Grão | Um registro por partido |
| Chave esperada | `id_partido` ou `sigla_partido` |

Colunas obrigatórias recomendadas:

- `id_partido`;
- `sigla_partido`;
- `nome_partido`.

Regras críticas:

- tabela não vazia;
- `sigla_partido` não nula;
- duplicidades devem ser controladas.

---

### Star — `dim_partido`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Silver/Gold partidos |
| Grão | Um registro por partido |
| Chave substituta | `sk_partido` |
| Chave de negócio | `id_partido` ou `sigla_partido` |

Colunas obrigatórias recomendadas:

- `sk_partido`;
- `id_partido`;
- `sigla_partido`;
- `nome_partido`.

Regras críticas:

- `sk_partido` único;
- `sigla_partido` não nula;
- domínio de siglas deve ser consistente.

---

## 5.3 Proposições

### Bronze — `proposicoes`

| Campo | Regra |
|---|---|
| Camada | Bronze |
| Origem | Endpoint de proposições da API da Câmara |
| Grão | Um registro por proposição retornada pela API |
| Chave esperada | `id` ou identificador equivalente da proposição |

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

---

### Silver — `proposicoes`

| Campo | Regra |
|---|---|
| Camada | Silver |
| Origem | Bronze `proposicoes` |
| Grão | Um registro padronizado por proposição |
| Chave esperada | `id_proposicao` |

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

---

### Gold — `proposicoes`

| Campo | Regra |
|---|---|
| Camada | Gold |
| Origem | Silver `proposicoes` + regras/ML |
| Grão | Um registro enriquecido por proposição |
| Chave esperada | `id_proposicao` |

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

---

### Star — `dim_proposicao`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `proposicoes` |
| Grão | Um registro por proposição |
| Chave substituta | `sk_proposicao` |
| Chave de negócio | `id_proposicao` |

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

---

### Star — `fato_proposicao`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `proposicoes` + dimensões relacionadas |
| Grão | Uma linha por proposição |
| Chave de fato | `id_proposicao` ou chave substituta equivalente |

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

---

## 5.4 Autores de proposições

### Silver/Gold — `proposicoes_autores`

| Campo | Regra |
|---|---|
| Camada | Silver/Gold |
| Origem | Endpoint dependente de autores por proposição |
| Grão | Um registro por relação entre proposição e autor |
| Chave esperada | combinação entre `id_proposicao` e identificador/nome do autor |

Colunas obrigatórias recomendadas:

- `id_proposicao`;
- `id_autor` ou campo equivalente;
- `nome_autor`;
- `tipo_autor`.

Regras críticas:

- `id_proposicao` não nulo;
- autor deve possuir identificador ou nome;
- relação duplicada deve ser controlada.

---

### Star — `fato_autoria`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `proposicoes_autores` + dimensões |
| Grão | Uma linha por relação autor-proposição |
| Chave composta | `sk_proposicao` + `sk_deputado` ou autor equivalente |

Colunas obrigatórias recomendadas:

- `sk_proposicao`;
- `sk_deputado` ou identificador de autor;
- `id_proposicao`;
- `nome_autor`;
- `tipo_autor`.

Regras críticas:

- `sk_proposicao` não nula;
- autor identificado por chave ou nome;
- relação autor-proposição não deve duplicar sem motivo analítico.

---

## 5.5 Tramitações

### Silver/Gold — `tramitacoes`

| Campo | Regra |
|---|---|
| Camada | Silver/Gold |
| Origem | Endpoint dependente de tramitações por proposição |
| Grão | Uma linha por movimentação de uma proposição |
| Chave esperada | combinação entre `id_proposicao`, data/hora e sequência quando disponível |

Colunas obrigatórias recomendadas:

- `id_proposicao`;
- `data_tramitacao`;
- `descricao_tramitacao`;
- `sigla_orgao` ou órgão equivalente;
- `status_tramitacao`, quando enriquecido.

Regras críticas:

- `id_proposicao` não nulo;
- data da tramitação deve existir quando disponível na origem;
- status ou descrição deve estar preenchido;
- duplicidades devem ser controladas.

---

### Star — `fato_tramitacao`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `tramitacoes` + dimensões |
| Grão | Uma linha por tramitação |
| Chave de relacionamento | `sk_proposicao`, `sk_tempo`, `sk_orgao` quando aplicável |

Colunas obrigatórias recomendadas:

- `sk_proposicao`;
- `sk_tempo`;
- `sk_orgao` ou identificador de órgão;
- `id_proposicao`;
- `descricao_tramitacao`;
- `status_tramitacao`.

Regras críticas:

- `sk_proposicao` não nula;
- relacionamento com `dim_proposicao` deve ser válido;
- o grão de uma linha por movimentação deve ser preservado.

---

## 5.6 Votações e votos

### Silver/Gold — `votacoes`

| Campo | Regra |
|---|---|
| Camada | Silver/Gold |
| Origem | Endpoint de votações |
| Grão | Uma linha por votação |
| Chave esperada | `id_votacao` |

Colunas obrigatórias recomendadas:

- `id_votacao`;
- `id_proposicao`, quando aplicável;
- `data_votacao`;
- `descricao_votacao`;
- `resultado_votacao`, quando disponível.

Regras críticas:

- `id_votacao` não nulo;
- `id_votacao` único;
- data ou descrição da votação deve existir.

---

### Silver/Gold — `votos`

| Campo | Regra |
|---|---|
| Camada | Silver/Gold |
| Origem | Endpoint dependente de votos por votação |
| Grão | Uma linha por voto parlamentar em uma votação |
| Chave esperada | combinação entre `id_votacao` e deputado/parlamentar |

Colunas obrigatórias recomendadas:

- `id_votacao`;
- `id_deputado` ou identificador equivalente;
- `nome_deputado`;
- `sigla_partido`;
- `sigla_uf`;
- `voto`.

Regras críticas:

- `id_votacao` não nulo;
- parlamentar deve estar identificado;
- campo `voto` deve existir;
- domínio de voto deve ser controlado.

Domínios recomendados para `voto`:

- `Sim`;
- `Não`;
- `Abstenção`;
- `Obstrução`;
- `Art. 17`;
- outros valores oficiais retornados pela API.

---

### Star — `fato_votacao`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `votacoes` + dimensões |
| Grão | Uma linha por votação |
| Chave esperada | `id_votacao` |

Colunas obrigatórias recomendadas:

- `id_votacao`;
- `sk_proposicao`;
- `sk_tempo`;
- `resultado_votacao`.

Regras críticas:

- `id_votacao` não nulo;
- relacionamento com proposição deve ser válido quando houver proposição associada.

---

### Star — `fato_voto`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `votos` + dimensões |
| Grão | Uma linha por voto parlamentar |
| Chave composta | `id_votacao` + `sk_deputado` |

Colunas obrigatórias recomendadas:

- `id_votacao`;
- `sk_deputado`;
- `sk_partido`;
- `sk_tempo`;
- `voto`.

Regras críticas:

- `id_votacao` não nulo;
- `voto` não nulo;
- domínio de voto válido;
- relacionamento com dimensões deve ser validado.

---

## 5.7 Órgãos

### Silver — `orgaos`

| Campo | Regra |
|---|---|
| Camada | Silver |
| Origem | Endpoint de órgãos da API |
| Grão | Um registro por órgão |
| Chave esperada | `id_orgao` ou `sigla_orgao` |

Colunas obrigatórias recomendadas:

- `id_orgao`;
- `sigla_orgao`;
- `nome_orgao`.

Regras críticas:

- identificador ou sigla do órgão deve existir;
- duplicidades devem ser controladas.

---

### Star — `dim_orgao`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Silver/Gold órgãos |
| Grão | Um registro por órgão |
| Chave substituta | `sk_orgao` |
| Chave de negócio | `id_orgao` ou `sigla_orgao` |

Colunas obrigatórias recomendadas:

- `sk_orgao`;
- `id_orgao`;
- `sigla_orgao`;
- `nome_orgao`.

Regras críticas:

- `sk_orgao` único;
- órgão identificado por chave ou sigla.

---

## 5.8 Eventos e presença

### Silver/Gold — `eventos`

| Campo | Regra |
|---|---|
| Camada | Silver/Gold |
| Origem | Endpoint de eventos da API |
| Grão | Uma linha por evento legislativo |
| Chave esperada | `id_evento` |

Colunas obrigatórias recomendadas:

- `id_evento`;
- `data_evento`;
- `descricao_evento`;
- `id_orgao` ou órgão relacionado;
- `situacao_evento`, quando disponível.

Regras críticas:

- `id_evento` não nulo;
- `id_evento` único;
- data ou descrição do evento deve existir.

---

### Silver/Gold — `presencas_eventos`

| Campo | Regra |
|---|---|
| Camada | Silver/Gold |
| Origem | Endpoint dependente de presença em eventos |
| Grão | Uma linha por presença de parlamentar em evento |
| Chave esperada | combinação entre `id_evento` e parlamentar |

Colunas obrigatórias recomendadas:

- `id_evento`;
- `id_deputado` ou identificador equivalente;
- `nome_deputado`;
- `sigla_partido`;
- `sigla_uf`;
- `situacao_presenca`, quando disponível.

Regras críticas:

- `id_evento` não nulo;
- parlamentar identificado por chave ou nome;
- duplicidades devem ser controladas.

---

### Star — `fato_evento`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `eventos` + dimensões |
| Grão | Uma linha por evento |
| Chave esperada | `id_evento` |

Colunas obrigatórias recomendadas:

- `id_evento`;
- `sk_tempo`;
- `sk_orgao`;
- `descricao_evento`;
- `situacao_evento`.

Regras críticas:

- `id_evento` não nulo;
- relacionamento com tempo e órgão deve ser validado quando disponível.

---

### Star — `fato_presenca`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Gold `presencas_eventos` + dimensões |
| Grão | Uma linha por presença parlamentar em evento |
| Chave composta | `id_evento` + parlamentar |

Colunas obrigatórias recomendadas:

- `id_evento`;
- `sk_deputado`;
- `sk_partido`;
- `sk_tempo`;
- `situacao_presenca`.

Regras críticas:

- `id_evento` não nulo;
- parlamentar identificado;
- relacionamento com `dim_deputado` deve ser validado quando disponível.

---

## 5.9 Tempo

### Star — `dim_tempo`

| Campo | Regra |
|---|---|
| Camada | Star Schema |
| Origem | Datas derivadas das tabelas analíticas |
| Grão | Uma linha por data |
| Chave substituta | `sk_tempo` |
| Chave de negócio | `data` |

Colunas obrigatórias recomendadas:

- `sk_tempo`;
- `data`;
- `ano`;
- `mes`;
- `nome_mes`;
- `trimestre`;
- `dia`;
- `dia_semana`.

Regras críticas:

- `sk_tempo` único;
- `data` única;
- `ano`, `mes` e `dia` não nulos;
- datas devem cobrir o intervalo necessário para as tabelas fato.

---

# 6. Severidade das regras

As regras podem ser classificadas em dois níveis principais.

## 6.1 Error

Regras do tipo `error` devem bloquear a continuação do pipeline ou impedir a publicação da tabela na camada Serving.

Exemplos:

- tabela vazia em etapa crítica;
- ausência de coluna obrigatória;
- chave primária nula;
- duplicidade em chave que deveria ser única;
- schema incompatível com a camada de consumo.

## 6.2 Warning

Regras do tipo `warning` não necessariamente bloqueiam o pipeline, mas devem gerar alerta e ser monitoradas.

Exemplos:

- percentual elevado de nulos em campo não crítico;
- categoria fora do domínio esperado;
- relacionamento ausente em pequena parcela dos registros;
- volume processado muito diferente da execução anterior.

---

# 7. Exemplo de contrato em formato declarativo

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

---

# 8. Integração com Data Quality

Os contratos documentados aqui devem orientar a camada de Data Quality do projeto.

A relação esperada é:

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

Exemplo de fluxo recomendado:

```text
1. Ler tabela produzida pela camada
2. Identificar contrato aplicável
3. Executar validações obrigatórias
4. Registrar resultado das validações
5. Bloquear avanço se houver erro crítico
6. Permitir avanço com alerta se houver apenas warnings
```

---

# 9. Boas práticas recomendadas

Para manter os contratos úteis e atualizados:

- atualizar este documento sempre que uma tabela mudar de schema;
- versionar mudanças relevantes de contrato;
- diferenciar regras críticas de regras de alerta;
- evitar regras excessivamente rígidas em campos naturalmente incompletos na API;
- priorizar chaves, colunas obrigatórias e integridade entre camadas;
- registrar exceções conhecidas;
- manter alinhamento entre contratos, código e documentação do Star Schema.

---

# 10. Próximas evoluções

Possíveis evoluções deste documento:

- transformar contratos em arquivos YAML executáveis;
- criar um registry formal de contratos por tabela;
- integrar contratos ao runner de cada camada;
- persistir resultados das validações em tabela Delta;
- criar dashboard operacional de qualidade de dados;
- aplicar bloqueio automático antes da camada Serving;
- adicionar validação de integridade referencial entre fatos e dimensões.

---

# 11. Conclusão

Os contratos de dados ajudam a tornar o projeto mais confiável, documentado e próximo de uma solução produtiva.

Mesmo sendo um projeto de portfólio, a documentação dos contratos demonstra preocupação com governança, qualidade, rastreabilidade e manutenção do pipeline de dados.
