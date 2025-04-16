import enum
import os

import ibis

from composable_dataloader.logger import logger


class QueryEngine(str, enum.Enum):
    DUCKDB = "duckdb"
    SPARK = "spark"
    SPARK_CONNECT = "spark_connect"
    REMOTE_EXECUTION = "remote_execution"


def get_spark(query_engine: QueryEngine = QueryEngine.SPARK):
    """Create or get a Spark session based on the specified query engine.

    Args:
        query_engine: The query engine to use (SPARK or SPARK_CONNECT)

    Returns:
        SparkSession: A configured Spark session

    Raises:
        ValueError: If an unsupported query engine is specified
        ImportError: If PySpark or Databricks Connect is not installed
    """
    if query_engine not in [QueryEngine.SPARK, QueryEngine.SPARK_CONNECT]:
        raise ValueError("query_engine must be either SPARK or SPARK_CONNECT")

    try:
        if query_engine == QueryEngine.SPARK_CONNECT:
            from databricks.connect import DatabricksSession

            if "DATABRICKS_HOST" not in os.environ:
                raise OSError("DATABRICKS_HOST environment variable not set")

            if "DATABRICKS_CLUSTER_ID" not in os.environ:
                raise OSError("DATABRICKS_CLUSTER_ID environment variable not set")

            host = os.environ["DATABRICKS_HOST"]
            cluster_id = os.environ["DATABRICKS_CLUSTER_ID"]

            return DatabricksSession.builder.remote(host=host, cluster_id=cluster_id).getOrCreate()
        else:
            from pyspark.sql import SparkSession

            return SparkSession.builder.getOrCreate()
    except ImportError as e:
        raise ImportError(f"{query_engine} requested but required package is not installed: {str(e)}") from e


def get_connection(query_engine: QueryEngine = QueryEngine.DUCKDB) -> ibis.BaseBackend | None:
    """
    Create Ibis connection for DuckDB or Spark.
    """
    logger.info(f"Creating Ibis connection for {query_engine}")

    if query_engine == QueryEngine.DUCKDB:
        logger.debug("Initializing DuckDB connection")
        return ibis.con.duckdb()

    elif query_engine in [QueryEngine.SPARK, QueryEngine.SPARK_CONNECT]:
        try:
            logger.debug(f"Initializing {query_engine} connection")
            spark = get_spark(query_engine=query_engine)
            return ibis.pyspark.connect(spark)
        except ImportError as e:
            logger.error(f"Failed to initialize {query_engine}: {str(e)}")
            raise ImportError(f"Required packages for {query_engine} are not installed: {str(e)}") from e
    elif query_engine == QueryEngine.REMOTE_EXECUTION:
        return None

    else:
        logger.error(f"Unsupported query engine: {query_engine}")
        raise ValueError(f"Unsupported query engine: {query_engine}")
