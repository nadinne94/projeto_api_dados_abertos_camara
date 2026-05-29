# ML/NLP Legislativo

Este documento descreve a arquitetura, estratégia, fluxo e limitações da camada de Machine Learning e NLP do projeto.

O objetivo da camada ML/NLP é classificar proposições legislativas a partir de textos como ementa, descrição e campos relacionados, enriquecendo a camada Gold e alimentando o modelo dimensional utilizado no Power BI.

## Visão Geral

O projeto utiliza uma abordagem híbrida de classificação textual combinando:

- pré-processamento de texto;
- dicionários temáticos;
- regras regex;
- geração de features;
- modelo supervisionado;
- thresholds de confiança;
- fallback para textos ambíguos;
- MLflow para rastreamento e versionamento.

O fluxo geral é:

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

## Objetivo da Classificação

A camada de ML/NLP busca enriquecer as proposições legislativas com classificações analíticas.

As principais classificações são:

| Classificação              | Descrição                                     |
| -------------------------- | --------------------------------------------- |
| `tema_ementa`              | Tema principal identificado na proposição     |
| `macrotema`                | Agrupamento analítico do tema                 |
| `natureza_juridica`        | Finalidade ou natureza jurídica da proposição |
| `tipo_documental`          | Tipo documental derivado da proposição        |
| `categoria_regimental`     | Categoria analítica/regimental                |
| `origem_tema`              | Origem da classificação temática              |
| `origem_natureza_juridica` | Origem da classificação jurídica              |

## Por que usar NLP neste projeto?

Os dados legislativos possuem textos ricos, especialmente em campos como:

* ementa;
* descrição;
* despacho;
* tipo da proposição;
* regime de tramitação;
* situação.

Esses textos permitem identificar padrões sobre:

* assunto da proposição;
* objetivo legislativo;
* impacto social ou econômico;
* tipo de ação normativa;
* área temática;
* relevância analítica.

Sem classificação textual, o modelo analítico ficaria limitado a contagens por tipo ou data. Com NLP, o projeto passa a responder perguntas mais ricas, como:

* Quais temas legislativos são mais frequentes?
* Quais deputados propõem mais projetos sobre saúde?
* Quais partidos concentram proposições econômicas?
* Quais temas aparecem mais em votações?
* Qual proporção das proposições tem caráter normativo?
* Quais propostas têm foco social, econômico ou fiscalizatório?

## Estrutura da Camada ML

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

## Responsabilidade dos Módulos

| Módulo                             | Responsabilidade                                  |
| ---------------------------------- | ------------------------------------------------- |
| `base/preprocessing.py`            | Normalização textual                              |
| `base/regex.py`                    | Aplicação de padrões regex                        |
| `base/scoring.py`                  | Cálculo de pontuação/confiança                    |
| `dictionaries/temas.py`            | Dicionário de temas legislativos                  |
| `dictionaries/natureza.py`         | Dicionário de natureza jurídica                   |
| `features/tema.py`                 | Geração de features e labels de tema              |
| `features/natureza.py`             | Geração de features e labels de natureza jurídica |
| `training/trainer.py`              | Treinamento dos modelos                           |
| `training/registry.py`             | Definição dos modelos e configurações             |
| `inference/udf_loader.py`          | Carregamento de modelo para inferência Spark      |
| `orchestration/training_runner.py` | Orquestração do treinamento                       |

# Pré-processamento Textual

O pré-processamento textual prepara os textos legislativos para classificação.

## Objetivos

* reduzir ruído;
* padronizar textos;
* melhorar matching por regex;
* melhorar qualidade das features;
* evitar diferenças artificiais causadas por acentos, pontuação ou caixa.

## Transformações comuns

| Etapa                      | Exemplo                                 |
| -------------------------- | --------------------------------------- |
| Converter para minúsculas  | `Educação Pública` → `educação pública` |
| Remover acentos            | `educação` → `educacao`                 |
| Remover pontuação          | `saúde!!!` → `saude`                    |
| Remover espaços duplicados | `meio   ambiente` → `meio ambiente`     |
| Tratar nulos               | `None` → `""`                           |

## Exemplo conceitual

```text
Texto original:
"Institui o Programa Nacional de Apoio à Educação Básica."

Texto normalizado:
"institui o programa nacional de apoio a educacao basica"
```

# Dicionários Legislativos

O projeto utiliza dicionários para apoiar a classificação.

## Dicionário de Temas

O dicionário de temas contém palavras, expressões e padrões associados a áreas legislativas.

Exemplos de temas:

* Saúde;
* Educação;
* Segurança Pública;
* Meio Ambiente;
* Economia;
* Trabalho;
* Direitos Humanos;
* Administração Pública;
* Tributação;
* Infraestrutura;
* Ciência e Tecnologia;
* Cultura;
* Agricultura;
* Previdência;
* Defesa;
* Transporte.

## Dicionário de Natureza Jurídica

O dicionário de natureza jurídica busca identificar a finalidade legislativa da proposição.

Exemplos de naturezas:

* alteração normativa;
* criação de política pública;
* revogação;
* regulamentação;
* autorização;
* concessão;
* fiscalização;
* homenagem;
* instituição de data comemorativa;
* declaração de utilidade pública;
* criação de programa;
* sanção ou penalidade.

# Regras Regex

As regras regex capturam padrões explícitos em textos legislativos.

## Exemplos de padrões

| Padrão textual                 | Interpretação possível       |
| ------------------------------ | ---------------------------- |
| `altera a lei`                 | Alteração normativa          |
| `revoga`                       | Revogação                    |
| `institui o programa`          | Criação de política pública  |
| `dispõe sobre`                 | Regulamentação genérica      |
| `concede`                      | Concessão                    |
| `declara de utilidade pública` | Reconhecimento institucional |
| `institui o dia nacional`      | Data comemorativa            |
| `cria o programa`              | Criação de programa          |
| `acrescenta dispositivo`       | Alteração normativa          |

## Vantagens das Regras

* interpretáveis;
* fáceis de auditar;
* boas para padrões explícitos;
* úteis como baseline;
* úteis para gerar labels iniciais;
* permitem fallback controlado.

## Limitações das Regras

* podem ser rígidas;
* exigem manutenção;
* não capturam bem contexto implícito;
* podem gerar conflitos entre categorias;
* podem refletir viés do dicionário;
* podem classificar mal textos muito genéricos.

# Modelo Supervisionado

A camada supervisionada complementa as regras.

## Objetivo

Treinar um modelo para generalizar padrões textuais e classificar proposições que não foram capturadas com segurança pelas regras.

## Estratégia provável

O fluxo de treinamento segue o padrão:

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

## Técnicas adequadas

Para este projeto, são adequadas técnicas como:

* TF-IDF;
* Logistic Regression;
* Linear SVM;
* Naive Bayes;
* Random Forest como baseline secundário.

A escolha de TF-IDF + Logistic Regression é apropriada para portfólio porque é:

* simples;
* explicável;
* rápida;
* forte como baseline;
* compatível com textos curtos;
* fácil de registrar no MLflow.

# Estratégia Híbrida

A estratégia híbrida combina regras e ML.

## Fluxo conceitual

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

## Benefícios

| Benefício          | Descrição                                        |
| ------------------ | ------------------------------------------------ |
| Interpretabilidade | Regex permite explicar classificações explícitas |
| Generalização      | ML cobre textos menos diretos                    |
| Controle de risco  | Thresholds evitam classificações forçadas        |
| Rastreabilidade    | Origem da classificação pode ser registrada      |
| Evolução gradual   | Dicionários e modelo podem evoluir separadamente |

---

## Campos recomendados para rastreabilidade

A tabela Gold deve preservar campos que ajudem a auditar a classificação:

| Campo                           | Descrição                           |
| ------------------------------- | ----------------------------------- |
| `tema_ementa`                   | Tema final atribuído                |
| `origem_tema`                   | Regex, ML ou fallback               |
| `score_tema`                    | Confiança da classificação temática |
| `natureza_juridica`             | Natureza final atribuída            |
| `origem_natureza_juridica`      | Regex, ML ou fallback               |
| `score_natureza_juridica`       | Confiança da classificação jurídica |
| `modelo_tema_versao`            | Versão do modelo de tema            |
| `modelo_natureza_versao`        | Versão do modelo de natureza        |
| `flag_tema_por_ml`              | Indica uso de ML                    |
| `flag_natureza_por_ml`          | Indica uso de ML                    |
| `flag_classificacao_automatica` | Indica classificação automatizada   |

---

# Thresholds e Fallback

Thresholds são usados para decidir se uma predição é confiável.

## Exemplos de thresholds

| Parâmetro                    | Descrição                                     |
| ---------------------------- | --------------------------------------------- |
| `TEMA_MIN_SCORE`             | Score mínimo para aceitar tema                |
| `TEMA_MIN_MARGIN`            | Margem mínima entre primeira e segunda classe |
| `NATUREZA_MIN_SCORE`         | Score mínimo para aceitar natureza jurídica   |
| `ML_TEMA_MIN_CONFIDENCE`     | Confiança mínima do modelo de tema            |
| `ML_NATUREZA_MIN_CONFIDENCE` | Confiança mínima do modelo de natureza        |

---

## Por que usar fallback?

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

Nesses casos, forçar uma categoria pode prejudicar a qualidade analítica.

## Fallback recomendado

Usar categorias como:

* `Tema Não Explícito`;
* `Natureza Não Explícita`;
* `Não Classificado`;
* `Classificação Indeterminada`.

O fallback é melhor do que uma classificação artificial.

---

# MLflow

O MLflow é usado para rastrear e versionar modelos.

## Objetivos

* registrar experimentos;
* armazenar métricas;
* armazenar parâmetros;
* versionar modelos;
* permitir reuso em inferência;
* documentar evolução dos modelos.

---

## Itens que devem ser registrados

### Parâmetros

* tipo do modelo;
* max_features do TF-IDF;
* n-grams;
* test_size;
* random_state;
* thresholds;
* versão do dicionário;
* data do treinamento.

### Métricas

* accuracy;
* precision macro;
* recall macro;
* f1 macro;
* f1 weighted;
* matriz de confusão;
* quantidade de classes;
* quantidade de registros de treino;
* quantidade de registros de teste.

### Artefatos

* matriz de confusão;
* classification report;
* exemplos de erros;
* lista de classes;
* versão dos dicionários;
* pipeline serializado.

---

# Métricas de Avaliação

Para classificação legislativa, a métrica principal recomendada é:

```text
F1 macro
```

## Por que F1 macro?

Porque temas legislativos tendem a ser desbalanceados.

Algumas classes podem ter muitos exemplos, como:

* Administração Pública;
* Saúde;
* Educação;
* Economia.

Outras podem ter poucos exemplos, como:

* Ciência e Tecnologia;
* Cultura;
* Defesa;
* Relações Exteriores.

A acurácia pode parecer boa mesmo quando o modelo ignora classes minoritárias.

---

## Métricas recomendadas

| Métrica               | Uso                                          |
| --------------------- | -------------------------------------------- |
| Accuracy              | Visão geral                                  |
| Precision macro       | Qualidade média das predições por classe     |
| Recall macro          | Capacidade de encontrar classes minoritárias |
| F1 macro              | Métrica principal balanceada                 |
| F1 weighted           | Métrica ponderada por volume                 |
| Matriz de confusão    | Diagnóstico de erros                         |
| Classification report | Análise detalhada por classe                 |

---

# Riscos e Limitações

## 1. Labels derivados de regex

Se o modelo for treinado com labels gerados por regras, ele pode aprender os vieses dessas regras.

### Impacto

O modelo não aprende uma verdade externa, mas uma aproximação da lógica definida nos dicionários.

### Mitigação

Criar uma base validada manualmente com amostras reais.

---

## 2. Classes desbalanceadas

Alguns temas aparecem muito mais do que outros.

### Impacto

O modelo pode favorecer temas majoritários.

### Mitigação

* usar métricas macro;
* balancear amostras;
* aplicar class_weight;
* avaliar por classe;
* aumentar exemplos de classes minoritárias.

---

## 3. Textos genéricos

Muitas proposições possuem ementas genéricas ou pouco informativas.

### Impacto

Classificações podem ficar imprecisas.

### Mitigação

* usar fallback;
* combinar ementa com outros campos;
* incluir despacho, tipo e descrição;
* registrar confiança da classificação.

---

## 4. Ambiguidade temática

Uma proposição pode tratar de múltiplos temas.

Exemplo:

```text
"Institui programa de educação ambiental nas escolas públicas."
```

Possíveis temas:

* Educação;
* Meio Ambiente.

### Mitigação

* registrar tema principal e tema secundário;
* usar classificação multilabel no futuro;
* usar score por classe.

---

## 5. Evolução do vocabulário

O vocabulário legislativo muda ao longo do tempo.

### Mitigação

* reprocessar periodicamente;
* versionar dicionários;
* monitorar queda de confiança;
* revisar amostras recentes.

---

# Auditoria da Classificação

Uma evolução importante é criar uma tabela de auditoria de classificações.

## Tabela sugerida

```text
gold.proposicoes_classificacao_auditoria
```

## Campos sugeridos

| Campo                    | Descrição                    |
| ------------------------ | ---------------------------- |
| `id_proposicao`          | Identificador da proposição  |
| `texto_classificado`     | Texto usado na classificação |
| `tema_predito`           | Tema atribuído               |
| `tema_score`             | Score do tema                |
| `tema_origem`            | Regex, ML ou fallback        |
| `natureza_predita`       | Natureza atribuída           |
| `natureza_score`         | Score da natureza            |
| `natureza_origem`        | Regex, ML ou fallback        |
| `modelo_tema_versao`     | Versão do modelo de tema     |
| `modelo_natureza_versao` | Versão do modelo de natureza |
| `dicionario_versao`      | Versão dos dicionários       |
| `classified_at`          | Timestamp da classificação   |

---

# Validação Manual

Para aumentar a credibilidade do projeto, recomenda-se criar uma pequena base manual.

## Tamanho inicial recomendado

```text
100 a 300 proposições
```

## Processo sugerido

1. Amostrar proposições de diferentes anos e tipos;
2. Classificar manualmente tema e natureza;
3. Comparar com regex;
4. Comparar com ML;
5. Comparar com abordagem híbrida;
6. Registrar métricas;
7. Documentar exemplos de acerto e erro.

---

## Benefícios para portfólio

Essa validação demonstra:

* pensamento crítico;
* preocupação com qualidade;
* entendimento de avaliação de ML;
* maturidade técnica;
* honestidade sobre limitações.

---

# Evolução para Embeddings

Uma evolução natural é usar embeddings semânticos.

## Possibilidades

* Sentence-BERT;
* embeddings multilíngues;
* embeddings OpenAI;
* similaridade semântica;
* clusterização de proposições;
* busca semântica.

## Casos de uso

* encontrar proposições semelhantes;
* detectar duplicidade semântica;
* sugerir temas;
* agrupar ementas;
* descobrir novos tópicos;
* comparar proposições entre anos.

---

# Evolução para LLMs

LLMs podem ser usados como camada complementar, não necessariamente como substituto do pipeline atual.

## Possíveis usos

* sumarização de proposições;
* explicação da classificação;
* extração de entidades;
* classificação assistida;
* geração de tags;
* identificação de impacto social;
* geração de texto explicativo para dashboard.

---

## Cuidados

* custo;
* latência;
* reprodutibilidade;
* privacidade;
* alucinação;
* necessidade de validação;
* versionamento de prompts;
* explicabilidade.

---

# Evolução para Classificação Multilabel

Atualmente, a classificação tende a atribuir um tema principal.

Mas proposições legislativas podem ter múltiplos temas.

## Exemplo

```text
"Cria programa de saúde mental nas escolas públicas."
```

Temas possíveis:

* Saúde;
* Educação;
* Direitos Humanos.

## Evolução recomendada

Criar uma classificação multilabel com:

* tema principal;
* temas secundários;
* score por tema;
* threshold por classe.

---

# Integração com a Camada Gold

A camada Gold é o ponto principal de aplicação da classificação.

## Fluxo

```text
silver.proposicoes
        ↓
transform_proposicoes
        ↓
classificação temática
        ↓
classificação de natureza jurídica
        ↓
flags analíticas
        ↓
gold.proposicoes
```

---

## Campos gerados na Gold

Exemplos de campos esperados:

| Campo                           | Descrição                         |
| ------------------------------- | --------------------------------- |
| `tema_ementa`                   | Tema final                        |
| `macrotema`                     | Agrupamento do tema               |
| `natureza_juridica`             | Natureza final                    |
| `tipo_documental`               | Tipo classificado                 |
| `categoria_regimental`          | Categoria analítica               |
| `origem_tema`                   | Origem da classificação           |
| `origem_natureza_juridica`      | Origem da classificação           |
| `flag_tema_por_ml`              | Indica se tema veio do ML         |
| `flag_natureza_por_ml`          | Indica se natureza veio do ML     |
| `flag_classificacao_automatica` | Indica classificação automatizada |

---

# Integração com Star Schema

A classificação alimenta a dimensão de proposição.

```text
gold.proposicoes
        ↓
star.dim_proposicao
        ↓
Power BI
```

## Uso na `dim_proposicao`

A dimensão `dim_proposicao` deve preservar atributos como:

* `tema_ementa`;
* `macrotema`;
* `natureza_juridica`;
* `tipo_documental`;
* `categoria_regimental`;
* `origem_tema`;
* `origem_natureza_juridica`;
* flags analíticas.

---

# Análises no Power BI

Com a classificação ML/NLP, o Power BI pode responder perguntas como:

* Proposições por tema;
* Proposições por macrotema;
* Proposições por natureza jurídica;
* Evolução de temas ao longo do tempo;
* Temas mais frequentes por partido;
* Temas mais frequentes por deputado;
* Votações por tema;
* Votos por tema;
* Eventos relacionados a determinados macrotemas;
* Proporção de proposições classificadas por ML;
* Proporção de proposições classificadas por regra.

---

# Data Quality para ML/NLP

A camada de ML/NLP também deve possuir validações.

## Validações recomendadas

| Validação               | Descrição                                           |
| ----------------------- | --------------------------------------------------- |
| Texto não vazio         | Verificar se há texto suficiente para classificação |
| Classe não nula         | Validar tema/natureza final                         |
| Score mínimo            | Validar confiança quando aplicável                  |
| Origem válida           | Validar origem da classificação                     |
| Domínio de temas        | Validar se tema pertence ao dicionário              |
| Domínio de natureza     | Validar se natureza pertence ao dicionário          |
| Distribuição de classes | Monitorar concentração excessiva em uma classe      |
| Drift textual           | Monitorar mudança de vocabulário ao longo do tempo  |

---

## Domínios recomendados

Campos como `origem_tema` podem ter domínio controlado:

```text
regex
ml
fallback
manual
```

Campos como `origem_natureza_juridica` também devem seguir domínio controlado.

---

# Testes Automatizados Recomendados

A camada ML/NLP deve possuir testes unitários.

## Testes de pré-processamento

* remove acentos;
* converte para minúsculas;
* remove pontuação;
* trata nulos;
* remove espaços duplicados.

## Testes de regex

* identifica tema esperado;
* identifica natureza esperada;
* não classifica texto genérico;
* resolve conflito por score;
* respeita fallback.

## Testes de inferência

* modelo carrega corretamente;
* UDF retorna estrutura esperada;
* scores estão dentro do intervalo esperado;
* fallback é aplicado quando score é baixo.

## Testes de integração

* transformação Gold gera campos de classificação;
* `dim_proposicao` preserva os campos classificados;
* Power BI consegue consumir os campos finais.

---

# Exemplo de Teste Manual

| Ementa                                                           | Tema esperado    | Natureza esperada           |
| ---------------------------------------------------------------- | ---------------- | --------------------------- |
| Institui programa de atenção à saúde mental nas escolas públicas | Saúde / Educação | Criação de política pública |
| Altera a Lei nº X para dispor sobre crimes ambientais            | Meio Ambiente    | Alteração normativa         |
| Institui o Dia Nacional de Conscientização sobre Doença Rara     | Saúde            | Data comemorativa           |
| Revoga dispositivo da legislação tributária                      | Tributação       | Revogação                   |
| Requer informações ao Ministério da Educação                     | Educação         | Fiscalização                |

---

# Boas Práticas Aplicadas

A camada ML/NLP segue boas práticas importantes:

* separação entre dicionários, features, treino e inferência;
* uso de regras interpretáveis;
* uso de modelo supervisionado como complemento;
* rastreabilidade da origem da classificação;
* uso de fallback;
* possibilidade de versionamento com MLflow;
* integração da classificação com camada analítica.

---

# Limitações Atuais

As principais limitações são:

* labels podem ser derivados de regras;
* ausência de base manual ampla;
* classificação tende a ser single-label;
* ementas podem ser genéricas;
* dicionários exigem manutenção;
* classes podem ser desbalanceadas;
* inferência depende de thresholds bem calibrados;
* métricas precisam ser avaliadas por classe.

Essas limitações são aceitáveis para um projeto de portfólio, desde que estejam documentadas.

---

# Roadmap ML/NLP

## Curto prazo

* documentar dicionários;
* adicionar testes de pré-processamento;
* adicionar testes de regex;
* registrar matriz de confusão no MLflow;
* registrar classification report;
* criar amostra manual de validação;
* criar tabela de auditoria de classificações.

---

## Médio prazo

* comparar regex, ML e abordagem híbrida;
* avaliar LinearSVC;
* aplicar class_weight;
* medir F1 macro por classe;
* monitorar distribuição de temas;
* criar relatório de erros;
* adicionar classificação multilabel;
* versionar dicionários.

---

## Longo prazo

* usar embeddings;
* criar busca semântica de proposições;
* aplicar clusterização temática;
* usar LLMs para sumarização;
* usar LLMs para classificação assistida;
* criar active learning;
* criar painel de monitoramento de qualidade do modelo;
* detectar drift textual;
* integrar com Feature Store.

---

# Recomendações para Apresentação em Entrevista

Ao explicar essa parte do projeto, uma boa resposta seria:

> A classificação legislativa foi construída com uma abordagem híbrida. Usei regras regex e dicionários para capturar padrões explícitos do texto legislativo, como alterações normativas, revogações e criação de programas. Para complementar, adicionei um modelo supervisionado com features textuais, registrado no MLflow, para generalizar casos menos óbvios. Também usei thresholds e fallback para evitar classificações forçadas quando o texto não tem informação suficiente.

---

## Pontos que demonstram maturidade

Na entrevista, vale enfatizar:

* o motivo de usar regex + ML;
* a importância da interpretabilidade;
* o uso de fallback;
* os riscos de labels derivados por regra;
* a necessidade de validação manual;
* a escolha de F1 macro;
* a integração com Gold e Star Schema;
* o uso de MLflow;
* as possibilidades de evolução com embeddings e LLMs.

---

# Resumo

A camada ML/NLP adiciona valor analítico ao projeto ao transformar textos legislativos em categorias estruturadas.

Ela permite que o pipeline responda perguntas mais ricas sobre temas, natureza jurídica e impacto das proposições.

A estratégia híbrida regex + ML é adequada para o domínio legislativo porque combina:

* interpretabilidade;
* controle;
* generalização;
* rastreabilidade;
* evolução gradual.

Com validação manual, testes automatizados, auditoria das classificações e métricas por classe, essa camada pode evoluir para um componente muito forte e diferenciado do projeto.
