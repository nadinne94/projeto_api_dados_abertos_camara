import time

from src.config.project_config import STORAGE_CONFIG
from src.utils.storage.delta_io import read_table
from src.gold.transforms.proposicoes import transform_proposicoes

df_silver = read_table(
    spark,
    STORAGE_CONFIG,
    "silver",
    "proposicoes"
)

print("silver count...")
t0 = time.time()
print(df_silver.count(), time.time() - t0)

print("transform...")
t0 = time.time()
df_gold_test = transform_proposicoes(df_silver)
print("transform lazy ok", time.time() - t0)

print("gold count...")
t0 = time.time()
print(df_gold_test.count(), time.time() - t0)