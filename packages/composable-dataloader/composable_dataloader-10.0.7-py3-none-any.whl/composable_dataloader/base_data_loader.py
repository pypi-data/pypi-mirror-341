import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Annotated

import ibis
from typer import Option

from composable_dataloader.dynamic_cli_mixin import DynamicCliMixin
from composable_dataloader.engine import QueryEngine, get_connection
from composable_dataloader.format import Format
from composable_dataloader.logger import logger
from composable_dataloader.output import (
    read_table,
    write_dataframe_to_stdout,
)


class Mode(str, enum.Enum):
    OVERWRITE = "overwrite"
    APPEND = "append"
    IGNORE = "ignore"


class StdoutMode(str, enum.Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


@dataclass
class DataLoader(DynamicCliMixin, ABC):
    """
    Base class for data loaders.

    Defines interface for creating data loaders that run Ibis queries
    and write results to storage or stdout.
    """

    def __post_init__(self):
        """Initialize Ibis connection based on configured query engine."""
        logger.info(f"Initializing {self.__class__.__name__} with {self.query_engine} engine")
        self.con = get_connection(query_engine=self.query_engine)

        if self.query_engine != QueryEngine.REMOTE_EXECUTION and not self.con:
            raise ConnectionError(f"Failed to establish connection with {self.query_engine} engine")

    output_location: Annotated[
        str,
        Option(
            ...,
            "--output-location",
            "--output_location",
            help="Location to write results",
            envvar="OUTPUT_LOCATION",
        ),
    ]

    stdout_mode: Annotated[
        StdoutMode,
        Option(
            StdoutMode.DISABLED,
            "--stdout-mode",
            "--stdout_mode",
            help="Whether to write results to stdout",
            envvar="STDOUT_MODE",
        ),
    ]

    account_name: Annotated[
        str,
        Option(
            ...,
            "--account-name",
            "--account_name",
            help="Account name for data access",
            envvar="ACCOUNT_NAME",
        ),
    ]

    write_mode: Annotated[
        Mode,
        Option(
            Mode.APPEND,
            "--write-mode",
            "--write_mode",
            help="Append, overwrite, ignore, error",
            envvar="WRITE_MODE",
        ),
    ]

    execution_mode: Annotated[
        str,
        Option(
            "dev",
            "--execution-mode",
            "--execution_mode",
            help="Execution mode (dev or prod)",
            envvar="EXECUTION_MODE",
        ),
    ]

    format: Annotated[
        Format,
        Option(
            Format.PARQUET,
            "--format",
            help="Output format (PARQUET or DELTA)",
            envvar="FORMAT",
        ),
    ]

    query_engine: Annotated[
        QueryEngine,
        Option(
            QueryEngine.SPARK_CONNECT,
            "--query-engine",
            "--query_engine",
            help="Query engine to use (REMOTE_EXECUTION, DUCKDB, SPARK, or SPARK_CONNECT)",
            rich_help_panel="Engine Options",
            case_sensitive=False,
            envvar="QUERY_ENGINE",
        ),
    ]

    def write_results_to_stdout(self) -> None:
        """
        Output result to stdout in Parquet format as required by Observable Framework.
        """
        logger.info(f"Streaming results from {self.output_location} to stdout for Observable Framework")

        table = read_table(
            uri=self.output_location,
            account_name=self.account_name,
            format=self.format,
        )
        write_dataframe_to_stdout(table)

    @abstractmethod
    def query(self) -> ibis.ir.Table:
        """
        Constructs and returns an Ibis query.

        This method should be implemented by subclasses to define the specific
        query logic for their data extraction needs.

        Returns:
            ibis.ir.Table: A lazily evaluated Ibis table expression

        Example:
            ```python
            def query(self):
                return self.con.table("my_table").filter(_.column > 10)
            ```
        """
        ...

    def execute_and_write(self) -> None:
        """Execute query and persist results to storage."""
        logger.info(f"Writing results to {self.output_location} ({self.format}, mode={self.write_mode})")

        result = self.query()

        if self.format == Format.PARQUET:
            result.to_parquet(self.output_location, mode=self.write_mode)
        elif self.format == Format.DELTA:
            result.to_delta(self.output_location, mode=self.write_mode)
        else:
            raise ValueError(f"Unsupported output format: {self.format}")
