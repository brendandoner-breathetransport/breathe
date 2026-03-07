import os
import re
from dataclasses import dataclass
from urllib.parse import urlparse

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


TABLE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$")


@dataclass
class _JdbcConfig:
    jdbc_url: str
    user: str
    password: str


class PostgresSparkIO:
    """Simple facade for Spark JDBC reads from Postgres.

    Usage:
      from civic_io import io
      df = io.read("analytics.mart_expense_share_monthly_income_annual")
    """

    def __init__(self, env_var: str = "DATABASE_URL") -> None:
        self.env_var = env_var

    def read(self, table_name: str, spark: SparkSession | None = None) -> DataFrame:
        if not TABLE_NAME_RE.match(table_name):
            raise ValueError(
                "Invalid table_name. Use 'schema.table' or 'table' with letters, numbers, and underscores."
            )

        spark_session = spark or SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
        cfg = self._load_jdbc_config()

        return (
            spark_session.read.format("jdbc")
            .option("url", cfg.jdbc_url)
            .option("dbtable", table_name)
            .option("user", cfg.user)
            .option("password", cfg.password)
            .option("driver", "org.postgresql.Driver")
            .load()
        )

    def _load_jdbc_config(self) -> _JdbcConfig:
        database_url = os.getenv(self.env_var)
        if not database_url:
            raise RuntimeError(f"Missing {self.env_var}.")

        parsed = urlparse(database_url)
        if parsed.scheme not in {"postgresql", "postgres"}:
            raise RuntimeError("DATABASE_URL must start with postgresql:// or postgres://")
        if not parsed.hostname or not parsed.username or parsed.password is None:
            raise RuntimeError("DATABASE_URL is missing host, username, or password.")

        port = parsed.port or 5432
        dbname = (parsed.path or "/").lstrip("/") or "postgres"
        jdbc_url = f"jdbc:postgresql://{parsed.hostname}:{port}/{dbname}"

        return _JdbcConfig(jdbc_url=jdbc_url, user=parsed.username, password=parsed.password)


io = PostgresSparkIO()
