"""
Treinamento e avaliação dos modelos de classificação textual.

Centraliza a execução do treinamento supervisionado, cálculo de métricas,
avaliação dos resultados e preparação dos artefatos para registro no
MLflow.

Este módulo contém a lógica principal de treinamento dos classificadores
usados no projeto.
"""


import pandas as pd

from pyspark.sql.functions import col

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from src.ml.training.pipeline import (
    create_pipeline
)


def prepare_training_data(
    df,
    target_col
):
    """Prepara os dados Spark para treinamento local do modelo.

    Parâmetros:
        df: DataFrame Spark com texto e coluna alvo.
        target_col: Nome da coluna de rótulo.

    Retorna:
        DataFrame Pandas com textos e rótulos tratados.
    """

    df = df.select(
        "ementa",
        target_col
    )

    df = df.filter(

        col("ementa").isNotNull()

        &

        col(target_col).isNotNull()
    )

    pdf = df.toPandas()

    if pdf.empty:

        raise ValueError(
            "Dataset vazio após leitura."
        )

    pdf["ementa"] = (

        pdf["ementa"]
        .astype(str)
        .str.strip()
    )

    pdf[target_col] = (

        pdf[target_col]
        .astype(str)
        .str.strip()
    )

    pdf = pdf[

        (pdf["ementa"] != "")

        &

        (pdf[target_col] != "")
    ]

    pdf = pdf.drop_duplicates(
        subset=["ementa", target_col]
    )

    if pdf.empty:

        raise ValueError(
            "Dataset vazio após limpeza."
        )

    return pdf


def balance_dataset(
    pdf,
    target_col,
    max_per_class=3000,
    min_per_class=10
):
    """Balanceia a base de treino limitando registros por classe.

    Parâmetros:
        pdf: DataFrame Pandas de entrada.
        target_col: Nome da coluna de rótulo.
        max_per_class: Quantidade máxima de registros mantidos por classe.
        min_per_class: Quantidade mínima de registros exigidos por classe.

    Retorna:
        DataFrame Pandas balanceado e embaralhado.
    """

    datasets = []

    for class_name, group in pdf.groupby(
        target_col
    ):

        total = len(group)

        if total < min_per_class:

            continue

        if total > max_per_class:

            group = group.sample(

                n=max_per_class,

                random_state=42
            )

        datasets.append(
            group
        )

    if not datasets:

        raise ValueError(
            "Nenhuma classe válida após balanceamento."
        )

    result = pd.concat(
        datasets,
        ignore_index=True
    )

    return result.sample(

        frac=1,

        random_state=42
    ).reset_index(
        drop=True
    )


def split_dataset(
    pdf,
    target_col,
    test_size=0.2
):
    """Divide a base rotulada em amostras de treino e teste.

    Parâmetros:
        pdf: DataFrame Pandas de entrada.
        target_col: Nome da coluna de rótulo.
        test_size: Fração usada para a amostra de teste.

    Retorna:
        Conjuntos de treino e teste gerados pelo scikit-learn.
    """

    X = pdf["ementa"]

    y = pdf[target_col]

    if y.nunique() < 2:

        raise ValueError(
            "Treino requer pelo menos 2 classes."
        )

    smallest_class_count = y.value_counts().min()

    stratify = y if smallest_class_count >= 2 else None

    return train_test_split(

        X,

        y,

        test_size=test_size,

        stratify=stratify,

        random_state=42
    )


def train_model(
    X_train,
    y_train
):

    pipeline = create_pipeline()

    pipeline.fit(
        X_train,
        y_train
    )

    return pipeline


def evaluate_model(
    pipeline,
    X_test,
    y_test
):

    predictions = pipeline.predict(
        X_test
    )

    labels = sorted(
        y_test.unique()
    )

    report = classification_report(

        y_test,

        predictions,

        output_dict=True,

        zero_division=0
    )

    confusion_matrix_values = confusion_matrix(

        y_test,

        predictions,

        labels=labels
    )

    confusion_matrix_df = pd.DataFrame(

        confusion_matrix_values,

        index=labels,

        columns=labels
    )

    return {

        "predictions": predictions,

        "report": report,

        "confusion_matrix": confusion_matrix_df,

        "labels": labels
    }


def run_training(
    df,
    target_col
):

    pdf = prepare_training_data(

        df,

        target_col
    )

    pdf = balance_dataset(

        pdf,

        target_col
    )

    X_train, X_test, y_train, y_test = split_dataset(

        pdf,

        target_col
    )

    pipeline = train_model(

        X_train,

        y_train
    )

    evaluation = evaluate_model(

        pipeline,

        X_test,

        y_test
    )

    return {

        "pipeline": pipeline,

        "report": evaluation["report"],

        "confusion_matrix": evaluation["confusion_matrix"],

        "predictions": evaluation["predictions"],

        "labels": evaluation["labels"],

        "X_test": X_test,

        "y_test": y_test,

        "target_col": target_col,

        "n_samples": len(pdf),

        "class_distribution": pdf[target_col].value_counts().to_dict()
    }