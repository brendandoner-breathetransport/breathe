import os
import re
from urllib.parse import urlparse

import polars as pl
import psycopg


TABLE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$")


class PostgresPolarsIO:
    """Simple facade for Polars reads from Postgres.

    Usage:
      from civic_io import io
      df = io.read("analytics.mart_expense_share_monthly_income_annual")
    """

    def __init__(self, env_var: str = "DATABASE_URL") -> None:
        self.env_var = env_var

    def list_objects(self, schema: str | None = None) -> pl.DataFrame:
        database_url = self._get_database_url()
        where_tables = "t.table_schema NOT IN ('pg_catalog', 'information_schema')"
        where_matviews = "m.schemaname NOT IN ('pg_catalog', 'information_schema')"

        if schema:
            schema_safe = schema.replace("'", "''")
            where_tables = f"t.table_schema = '{schema_safe}'"
            where_matviews = f"m.schemaname = '{schema_safe}'"

        query = f"""
            SELECT
                t.table_schema AS schema_name,
                t.table_name AS object_name,
                t.table_type AS object_type
            FROM information_schema.tables t
            WHERE {where_tables}
            UNION ALL
            SELECT
                m.schemaname AS schema_name,
                m.matviewname AS object_name,
                'MATERIALIZED VIEW' AS object_type
            FROM pg_catalog.pg_matviews m
            WHERE {where_matviews}
            ORDER BY schema_name, object_type, object_name
        """
        with psycopg.connect(database_url) as conn:
            return pl.read_database(query=query, connection=conn)

    def read(self, table_name: str, numeric_as_float: bool = True) -> pl.DataFrame:
        if not TABLE_NAME_RE.match(table_name):
            raise ValueError(
                "Invalid table_name. Use 'schema.table' or 'table' with letters, numbers, and underscores."
            )

        database_url = self._get_database_url()
        with psycopg.connect(database_url) as conn:
            query = self._build_select_query(conn, table_name, numeric_as_float=numeric_as_float)
            return pl.read_database(query=query, connection=conn)

    def _get_database_url(self) -> str:
        database_url = os.getenv(self.env_var)
        if not database_url:
            raise RuntimeError(f"Missing {self.env_var}.")

        parsed = urlparse(database_url)
        if parsed.scheme not in {"postgresql", "postgres"}:
            raise RuntimeError("DATABASE_URL must start with postgresql:// or postgres://")
        if not parsed.hostname:
            raise RuntimeError("DATABASE_URL is missing a host.")

        return database_url

    def _build_select_query(self, conn: psycopg.Connection, table_name: str, numeric_as_float: bool) -> str:
        schema_name, rel_name = self._split_table_name(table_name)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
                """,
                (schema_name, rel_name),
            )
            columns = cur.fetchall()

        if not columns:
            raise RuntimeError(f"Table not found or has no columns: {schema_name}.{rel_name}")

        select_exprs = []
        for column_name, data_type in columns:
            quoted_col = self._quote_ident(column_name)
            if numeric_as_float and data_type in {"numeric", "decimal"}:
                select_exprs.append(f"CAST({quoted_col} AS DOUBLE PRECISION) AS {quoted_col}")
            else:
                select_exprs.append(quoted_col)

        quoted_schema = self._quote_ident(schema_name)
        quoted_table = self._quote_ident(rel_name)
        return f"SELECT {', '.join(select_exprs)} FROM {quoted_schema}.{quoted_table}"

    @staticmethod
    def _split_table_name(table_name: str) -> tuple[str, str]:
        if "." in table_name:
            return tuple(table_name.split(".", 1))
        return "public", table_name

    @staticmethod
    def _quote_ident(identifier: str) -> str:
        return '"' + identifier.replace('"', '""') + '"'


io = PostgresPolarsIO()
