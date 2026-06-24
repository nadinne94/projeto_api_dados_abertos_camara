"""
Construção do pipeline de Machine Learning.

Centraliza a criação dos componentes de vetorização, transformação de
features e estimadores usados no treinamento dos classificadores textuais.

Este módulo padroniza a estrutura dos pipelines supervisionados usados
para classificação de tema e natureza jurídica.
"""


from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.calibration import (
    CalibratedClassifierCV
)


def criar_pipeline():

    base_classifier = LogisticRegression(

        max_iter=2000,

        class_weight="balanced",

        C=1.0,

        n_jobs=-1,

        random_state=42
    )

    return Pipeline([

        (

            "tfidf",

            TfidfVectorizer(

                max_features=20000,

                ngram_range=(1, 2),

                min_df=1,

                lowercase=True,

                strip_accents="unicode",

                sublinear_tf=True
            )
        ),

        (

            "clf",

            CalibratedClassifierCV(

                estimator=base_classifier,

                method="sigmoid",

                cv=3
            )
        )
    ])