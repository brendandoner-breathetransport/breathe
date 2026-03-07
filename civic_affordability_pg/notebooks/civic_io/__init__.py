from .core import PostgresPolarsIO, io

# Backward-compatible alias for older notebook imports.
PostgresSparkIO = PostgresPolarsIO

__all__ = ["PostgresPolarsIO", "PostgresSparkIO", "io"]
