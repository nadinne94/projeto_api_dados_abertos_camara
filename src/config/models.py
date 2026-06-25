"""
Configuração dos modelos de Machine Learning.

Centraliza os nomes, aliases e parâmetros relacionados aos modelos
utilizados na classificação textual de proposições legislativas.

As configurações podem ser carregadas a partir de variáveis de ambiente,
permitindo ajustar nomes de modelos e aliases sem alterar o código.
"""

from src.ml.config.training_configs import (
    CLASSIFICADORES_PROPOSICOES,
)


MODELS = CLASSIFICADORES_PROPOSICOES