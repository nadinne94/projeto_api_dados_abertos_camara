"""
Spark / Delta configuration.
"""

SPARK_CONFIG = {

    # Delta

    "spark.databricks.delta.schema.autoMerge.enabled":
        "true",

    # AQE

    "spark.sql.adaptive.enabled":
        "true",

    # Bronze workloads (API)

    "spark.sql.shuffle.partitions":
        "50"
}