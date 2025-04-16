"""
Framework for building data loaders with Ibis queries.

Supports running data loaders via CLI with DuckDB/Spark Connect
or as Databricks Asset Bundle (DAB) workflows.
"""

# Core components
# Make commonly used Typer components available
from typing import Annotated

from typer import Option

from composable_dataloader.base_data_loader import DataLoader, Mode

# Specialized loaders
from composable_dataloader.databricks import DatabricksDataLoader
from composable_dataloader.engine import QueryEngine, get_connection
from composable_dataloader.format import Format
from composable_dataloader.logger import logger

# Convenience exports
__all__ = [
    # Core components
    "DataLoader",
    "DatabricksDataLoader",
    "QueryEngine",
    "Format",
    "Mode",
    "logger",
    # Utilities
    "get_connection",
    # Type annotations
    "Annotated",
    "Option",
]
