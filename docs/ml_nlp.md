# ML/NLP Legislativo

## Objetivo

Este documento descreve a arquitetura, a estratégia, o fluxo e as limitações da camada de Machine Learning e NLP do projeto `projeto_api_dados_abertos_camara`.

O objetivo da camada ML/NLP é classificar proposições legislativas a partir de textos como ementa, descrição e campos relacionados, enriquecendo a camada Gold e alimentando o modelo dimensional utilizado no Power BI.

---

## Contexto

Os dados legislativos possuem textos ricos, especialmente em campos como:

- ementa;
- descrição;
- despacho;
- tipo da proposição;
- regime de tramitação;
- situação.

Esses textos permitem identificar padrões sobre assunto, objetivo legislativo, impacto social ou econômico, tipo de ação normativa e relevância analítica.

Sem classificação textual, o modelo analítico ficaria limitado a contagens por tipo, data ou entidade. Com NLP, o projeto passa a responder perguntas mais ricas, como:

- Quais temas legislativos são mais frequentes?
- Quais deputados propõem mais projetos sobre saúde?
- Quais partidos concentram proposições econômicas?
- Quais temas aparecem mais em votações?
- Qual proporção das proposições tem caráter normativo?
- Quais propostas têm foco social, econômico ou fiscalizatório?

---

## Escopo

Este documento cobre:

- visão geral da camada ML/NLP;
- objetivo da classificação;
- estrutura da camada ML;
- responsabilidades dos módulos;
- pré-processamento textual;
- dicionários legislativos;
- regras regex;
- modelo supervisionado;
- estratégia híbrida;
- thresholds e fallback;
- MLflow;
- inferência na camada Gold;
- rastreabilidade da classificação;
- limitações e evoluções futuras.

Este documento não detalha a implementação linha a linha dos modelos nem substitui a documentação de contratos de dados, Star Schema ou dashboard.

---

## Conteúdo Principal

### 1. Visão geral

O projeto utiliza uma abordagem híbrida de classificação textual combinando:

- pré-processamento de texto;
- dicionários temáticos;
- regras regex;
- geração de features;
- modelo supervisionado;
- thresholds de confiança;
- fallback para textos ambíguos;
- MLflow para rastreamento e versionamento.

Fluxo geral:

```text
Silver Proposições
        ↓
Pré-processamento textual
        ↓
Regras regex + dicionários
        ↓
Geração de labels/features
        ↓
Treinamento supervisionado
        ↓
MLflow Tracking
        ↓
MLflow Model Registry
        ↓
Inferência
        ↓
Gold Proposições
        ↓
dim_proposicao
        ↓
Power BI
```

### 2. Objetivo da classificação

A camada de ML/NLP busca enriquecer as proposições legislativas com classificações analíticas.

Principais classificações:

| Classificação | Descrição |
|---|---|
| `tema_ementa` | Tema principal identificado na proposição. |
| `macrotema` | Agrupamento analítico do tema. |
| `natureza_juridica` | Finalidade ou natureza jurídica da proposição. |
| `tipo_documental` | Tipo documental derivado da proposição. |
| `categoria_regimental` | Categoria analítica/regimental. |
| `origem_tema` | Origem da classificação temática. |
| `origem_natureza_juridica` | Origem da classificação jurídica. |

### 3. Estrutura da camada ML

A camada ML/NLP é organizada em módulos especializados.

```text
src/ml/
  base/
    preprocessing.py
    regex.py
    scoring.py

  dictionaries/
    temas.py
    natureza.py

  features/
    tema.py
    natureza.py

  training/
    trainer.py
    registry.py

  inference/
    udf_loader.py

  orchestration/
    training_runner.py
```

Responsabilidades:

| Módulo | Responsabilidade |
|---|---|
| `base/preprocessing.py` | Normalização textual. |
| `base/regex.py` | Aplicação de padrões regex. |
| `base/scoring.py` | Cálculo de pontuação/confiança. |
| `dictionaries/temas.py` | Dicionário de temas legislativos. |
| `dictionaries/natureza.py` | Dicionário de natureza jurídica. |
| `features/tema.py` | Geração de features e labels de tema. |
| `features/natureza.py` | Geração de features e labels de natureza jurídica. |
| `training/trainer.py` | Treinamento dos modelos. |
| `training/registry.py` | Definição dos modelos e configurações. |
| `inference/udf_loader.py` | Carregamento de modelo para inferência Spark. |
| `orchestration/training_runner.py` | Orquestração do treinamento. |

### 4. Pré-processamento textual

O pré-processamento textual prepara os textos legislativos para classificação.

Objetivos:

- reduzir ruído;
- padronizar textos;
- melhorar matching por regex;
- melhorar qualidade das features;
- evitar diferenças artificiais causadas por acentos, pontuação ou caixa.

Transformações comuns:

| Etapa | Exemplo |
|---|---|
| Converter para minúsculas | `Educação Pública` → `educação pública` |
| Remover acentos | `educação` → `educacao` |
| Remover pontuação | `saúde!!!` → `saude` |
| Remover espaços duplicados | `meio   ambiente` → `meio ambiente` |
| Tratar nulos | `None` → `""` |

Exemplo conceitual:

```text
Texto original:
"Institui o Programa Nacional de Apoio à Educação Básica."

Texto normalizado:
"institui o programa nacional de apoio a educacao basica"
```

### 5. Dicionários legislativos

O projeto utiliza dicionários para apoiar a classificação.

#### Dicionário de temas

O dicionário de temas contém palavras, expressões e padrões associados a áreas legislativas.

Exemplos de temas:

- Saúde;
- Educação;
- Segurança Pública;
- Meio Ambiente;
- Economia;
- Trabalho;
- Direitos Humanos;
- Administração Pública;
- Tributação;
- Infraestrutura;
- Ciência e Tecnologia;
- Cultura;
- Agricultura;
- Previdência;
- Defesa;
- Transporte.

#### Dicionário de natureza jurídica

O dicionário de natureza jurídica busca identificar a finalidade legislativa da proposição.

Exemplos de naturezas:

- alteração normativa;
- criação de política pública;
- revogação;
- regulamentação;
- autorização;
- concessão;
- fiscalização;
- homenagem;
- instituição de data comemorativa;
- declaração de utilidade pública;
- criação de programa;
- sanção ou penalidade.

### 6. Regras regex

As regras regex capturam padrões explícitos em textos legislativos.

Exemplos de padrões:

| Padrão textual | Interpretação possível |
|---|---|
| `altera a lei` | Alteração normativa. |
| `revoga` | Revogação. |
| `institui o programa` | Criação de política pública. |
| `dispõe sobre` | Regulamentação genérica. |
| `concede` | Concessão. |
| `declara de utilidade pública` | Reconhecimento institucional. |
| `institui o dia nacional` | Data comemorativa. |
| `cria o programa` | Criação de programa. |
| `acrescenta dispositivo` | Alteração normativa. |

Vantagens:

- interpretáveis;
- fáceis de auditar;
- boas para padrões explícitos;
- úteis como baseline;
- úteis para gerar labels iniciais;
- permitem fallback controlado.

Limitações:

- podem ser rígidas;
- exigem manutenção;
- não capturam bem contexto implícito;
- podem gerar conflitos entre categorias;
- podem refletir viés do dicionário;
- podem classificar mal textos muito genéricos.

### 7. Modelo supervisionado

A camada supervisionada complementa as regras.

Objetivo:

Treinar um modelo para generalizar padrões textuais e classificar proposições que não foram capturadas com segurança pelas regras.

Fluxo de treinamento:

```text
Texto normalizado
      ↓
TF-IDF
      ↓
Modelo supervisionado
      ↓
Predição de classe
      ↓
Score/confiança
```

Técnicas adequadas:

- TF-IDF;
- Logistic Regression;
- Linear SVM;
- Naive Bayes;
- Random Forest como baseline secundário.

A escolha de TF-IDF + Logistic Regression é apropriada para portfólio porque é:

- simples;
- explicável;
- rápida;
- forte como baseline;
- compatível com textos curtos;
- fácil de registrar no MLflow.

### 8. Estratégia híbrida

A estratégia híbrida combina regras e ML.

Fluxo conceitual:

```text
Texto da proposição
      ↓
Pré-processamento
      ↓
Classificação por regex/dicionário
      ↓
Regex tem alta confiança?
      ├── Sim → usa classificação por regra
      └── Não → aplica modelo ML
                    ↓
              ML tem confiança suficiente?
                    ├── Sim → usa classificação ML
                    └── Não → usa fallback
```

Benefícios:

| Benefício | Descrição |
|---|---|
| Interpretabilidade | Regex permite explicar classificações explícitas. |
| Generalização | ML cobre textos menos diretos. |
| Controle de risco | Thresholds evitam classificações forçadas. |
| Rastreabilidade | Origem da classificação pode ser registrada. |
| Evolução gradual | Dicionários e modelo podem evoluir separadamente. |

### 9. Campos de rastreabilidade

A tabela Gold deve preservar campos que ajudem a auditar a classificação.

| Campo | Descrição |
|---|---|
| `tema_ementa` | Tema final atribuído. |
| `origem_tema` | Regex, ML ou fallback. |
| `score_tema` | Confiança da classificação temática. |
| `natureza_juridica` | Natureza final atribuída. |
| `origem_natureza_juridica` | Regex, ML ou fallback. |
| `score_natureza_juridica` | Confiança da classificação jurídica. |
| `modelo_tema_versao` | Versão do modelo de tema. |
| `modelo_natureza_versao` | Versão do modelo de natureza. |
| `flag_tema_por_ml` | Indica uso de ML. |
| `flag_natureza_por_ml` | Indica uso de ML. |
| `flag_classificacao_automatica` | Indica classificação automatizada. |

### 10. Thresholds e fallback

Thresholds são usados para decidir se uma predição é confiável.

Exemplos:

| Parâmetro | Descrição |
|---|---|
| `TEMA_MIN_SCORE` | Score mínimo para aceitar tema. |
| `TEMA_MIN_MARGIN` | Margem mínima entre primeira e segunda classe. |
| `NATUREZA_MIN_SCORE` | Score mínimo para aceitar natureza jurídica. |
| `ML_TEMA_MIN_CONFIDENCE` | Confiança mínima do modelo de tema. |
| `ML_NATUREZA_MIN_CONFIDENCE` | Confiança mínima do modelo de natureza. |

Nem toda proposição possui texto suficiente para uma classificação segura.

Exemplos de textos problemáticos:

```text
"Dispõe sobre providências."
```

```text
"Altera dispositivo da legislação vigente."
```

```text
"Requer informações ao Ministério."
```

Nesses casos, forçar uma categoria pode prejudicar a análise. O fallback permite registrar uma categoria neutra, como:

- `Tema Não Explícito`;
- `Natureza Não Identificada`;
- `Outros Tipos`.

### 11. MLflow

O MLflow apoia rastreamento, versionamento e reutilização dos modelos.

Usos principais:

- registrar experimentos;
- armazenar parâmetros;
- armazenar métricas;
- versionar modelos;
- carregar modelos para inferência;
- registrar alias de produção, como `champion`.

Fluxo conceitual:

```text
Treinamento
   ↓
MLflow Tracking
   ↓
Model Registry
   ↓
Alias champion
   ↓
Inferência na Gold
```

### 12. Inferência na camada Gold

A inferência ocorre durante o enriquecimento analítico da camada Gold.

Fluxo esperado:

```text
Silver proposicoes
      ↓
Transformação Gold
      ↓
Aplicação de regras
      ↓
Aplicação de modelo ML quando necessário
      ↓
Fallback quando necessário
      ↓
Gold proposicoes enriquecida
```

A camada Gold deve registrar não apenas a classificação final, mas também a origem da classificação.

### 13. Avaliação do modelo

Para evolução do projeto, recomenda-se avaliar os modelos com métricas formais.

Métricas recomendadas:

- acurácia;
- precisão por classe;
- recall por classe;
- F1-score por classe;
- matriz de confusão;
- cobertura por classe;
- percentual de fallback;
- percentual classificado por regra;
- percentual classificado por ML.

### 14. Limitações conhecidas

Limitações naturais da abordagem:

- classes com poucos exemplos podem ter menor desempenho;
- textos curtos e genéricos podem exigir fallback;
- regras exigem manutenção contínua;
- dicionários podem gerar vieses de classificação;
- categorias legislativas podem se sobrepor;
- modelos clássicos com TF-IDF podem ter menor compreensão semântica que embeddings ou modelos de linguagem.

### 15. Possibilidades analíticas geradas

A classificação ML/NLP permite análises como:

- proposições por tema;
- proposições por natureza jurídica;
- macrotemas por ano;
- temas por partido;
- temas por deputado;
- classificação por origem: regra, ML ou fallback;
- cobertura da classificação automática;
- comparação entre temas e votações;
- análise de evolução temática por legislatura.

---

## Como este documento se conecta ao projeto

Este documento é a referência principal para a camada de classificação textual do projeto.

Ele se conecta diretamente a:

- `README.md`, que apresenta ML/NLP como diferencial técnico;
- `docs/architecture.md`, que posiciona ML/NLP entre Silver, Gold e Star Schema;
- `docs/execution_guide.md`, que explica quando executar o treinamento ML;
- `docs/data_contracts.md`, que documenta campos esperados de classificação;
- `docs/star_schema.md`, que usa as classificações em `dim_proposicao`;
- `docs/dashboard.md`, que consome as classificações em análises Power BI;
- `docs/dax_measures.md`, que sugere métricas de cobertura e qualidade analítica.

---

## Referências relacionadas

- [README do Projeto](../README.md)
- [Arquitetura do Projeto](architecture.md)
- [Guia de Execução](execution_guide.md)
- [Contratos de Dados](data_contracts.md)
- [Modelo Star Schema](star_schema.md)
- [Dashboard Power BI](dashboard.md)
- [Medidas DAX](dax_measures.md)
- [Qualidade de Dados](data_quality.md)
- [Evolução do Projeto](project_evolution.md)

---

## Próximas evoluções

Possíveis evoluções da camada ML/NLP:

- ampliar a base de treinamento;
- revisar classes com baixa representatividade;
- medir precisão, recall e F1-score por classe;
- gerar matriz de confusão;
- registrar métricas no MLflow;
- comparar modelos clássicos com embeddings;
- testar modelos de linguagem para classificação semântica;
- criar avaliação manual de amostras classificadas;
- reduzir conflitos entre temas semelhantes;
- versionar datasets de treino;
- documentar critérios mínimos para promover modelo ao alias `champion`;
- ampliar a classificação para legislaturas antigas.
