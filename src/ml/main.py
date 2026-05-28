from src.ml.config.training_configs import (
    CLASSIFICADORES_PROPOSICOES
)

from src.ml.orchestration.training_runner import (
    executar_lote_treinamento
)


EXPERIMENT_NAME = (

    "/Shared/"
    "api_dados_abertos_ml"

)


def main():

    executar_lote_treinamento(

        configs=CLASSIFICADORES_PROPOSICOES,

        experiment_name=EXPERIMENT_NAME
    )


if __name__ == "__main__":

    main()