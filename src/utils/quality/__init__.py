"""
Módulo de Data Quality.

Este pacote centraliza validações formais de qualidade de dados usadas
nas camadas Bronze, Silver, Gold e Star.

A proposta é permitir que cada tabela tenha um contrato declarativo com
regras mínimas de qualidade, como:

- existência de colunas obrigatórias;
- dataset não vazio;
- chaves não nulas;
- unicidade de chaves;
- limites de valores nulos;
- domínios permitidos;
- valores mínimos e máximos;
- validações de volume.
"""