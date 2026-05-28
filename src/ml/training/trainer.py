import pandas as pd

from pyspark.sql.functions import col

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from src.ml.training.pipeline import (
    criar_pipeline
)


def preparar_dados(
    df,
    target_col
):

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


def balancear_dataset(
    pdf,
    target_col,
    max_por_classe=3000,
    min_por_classe=10
):

    datasets = []

    for classe, grupo in pdf.groupby(
        target_col
    ):

        total = len(grupo)

        if total < min_por_classe:

            continue

        if total > max_por_classe:

            grupo = grupo.sample(

                n=max_por_classe,

                random_state=42
            )

        datasets.append(
            grupo
        )

    if not datasets:

        raise ValueError(
            "Nenhuma classe válida após balanceamento."
        )

    resultado = pd.concat(
        datasets,
        ignore_index=True
    )

    return resultado.sample(

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

    X = pdf["ementa"]

    y = pdf[target_col]

    if y.nunique() < 2:

        raise ValueError(
            "Treino requer pelo menos 2 classes."
        )

    menor_classe = y.value_counts().min()

    stratify = y if menor_classe >= 2 else None

    return train_test_split(

        X,

        y,

        test_size=test_size,

        stratify=stratify,

        random_state=42
    )


def treinar_modelo(
    X_train,
    y_train
):

    pipeline = criar_pipeline()

    pipeline.fit(
        X_train,
        y_train
    )

    return pipeline


def avaliar_modelo(
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

    matriz_confusao = confusion_matrix(

        y_test,

        predictions,

        labels=labels
    )

    matriz_confusao_df = pd.DataFrame(

        matriz_confusao,

        index=labels,

        columns=labels
    )

    return {

        "predictions": predictions,

        "report": report,

        "confusion_matrix": matriz_confusao_df,

        "labels": labels
    }


def executar_treino(
    df,
    target_col
):

    pdf = preparar_dados(

        df,

        target_col
    )

    pdf = balancear_dataset(

        pdf,

        target_col
    )

    X_train, X_test, y_train, y_test = split_dataset(

        pdf,

        target_col
    )

    pipeline = treinar_modelo(

        X_train,

        y_train
    )

    avaliacao = avaliar_modelo(

        pipeline,

        X_test,

        y_test
    )

    return {

        "pipeline": pipeline,

        "report": avaliacao["report"],

        "confusion_matrix": avaliacao["confusion_matrix"],

        "predictions": avaliacao["predictions"],

        "labels": avaliacao["labels"],

        "X_test": X_test,

        "y_test": y_test,

        "target_col": target_col,

        "n_samples": len(pdf),

        "class_distribution": pdf[target_col].value_counts().to_dict()
    }