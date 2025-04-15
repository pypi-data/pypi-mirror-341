import enum
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Self

import yaml
from azure.identity import DefaultAzureCredential
from databricks.sdk import WorkspaceClient
from databricks.sdk.config import Config
from databricks.sdk.credentials_provider import CredentialsProvider, CredentialsStrategy
from typer import Option

from composable_dataloader.base_data_loader import DataLoader, StdoutMode
from composable_dataloader.engine import QueryEngine
from composable_dataloader.logger import logger


class DabMode(str, enum.Enum):
    """Controls whether to execute via Databricks Asset Bundle (DAB) job or directly."""

    ENABLED = "enabled"  # Submit as a separate DAB job
    DISABLED = "disabled"  # Execute directly in the current process


@dataclass
class DatabricksDataLoader(DataLoader):
    """
    Data loader with Databricks Asset Bundle (DAB) support.

    Adds functionality to run queries via Databricks jobs.
    When DAB mode is enabled, this loader submits a separate job through
    the Databricks Asset Bundle system rather than running in the current process.
    """

    databricks_host: Annotated[
        str,
        Option(
            ...,
            "--databricks-host",
            "--databricks_host",
            help="Databricks host URL",
            envvar="DATABRICKS_HOST",
        ),
    ]

    dab: Annotated[
        DabMode,
        Option(
            DabMode.DISABLED,
            "--dab",
            help="Execute as Databricks Asset Bundle (enabled/disabled)",
            envvar="DAB",
        ),
    ]

    yaml_path: Annotated[
        Path,
        Option(
            "databricks.yml",
            "--yaml-path",
            "--yaml_path",
            help="Path to databricks.yml file",
            envvar="YML_CONFIG_FILE_PATH",
        ),
    ]

    def __post_init__(self) -> None:
        """
        Initialize base loader and set up Databricks client if needed.

        The client is initialized for DAB execution to interact with Databricks jobs.
        """

        super().__post_init__()

        # Initialize client if using Databricks Asset Bundle mode
        if self.dab == DabMode.ENABLED:
            logger.info(f"Initializing Databricks client for {self.execution_mode} mode")

            # Use client ID from environment if available
            client_id = os.getenv("AZURE_CLIENT_ID")
            logger.info(f"Using Azure credentials with client ID: {client_id}")

            self.client = WorkspaceClient(
                host=self.databricks_host,
                credentials_strategy=AzureIdentityCredentialsStrategy(client_id=client_id),
            )

    def get_job_name(self) -> str:
        """
        Get job name from Databricks Asset Bundle configuration.

        For development mode, includes the username to prevent job conflicts.

        Returns:
            str: Formatted job name based on bundle config

        Raises:
            FileNotFoundError: If the yaml_path doesn't exist
        """
        if not self.yaml_path.exists():
            raise FileNotFoundError(f"Could not find yml at {self.yaml_path}")

        with open(self.yaml_path) as file:
            config = yaml.safe_load(file)

        bundle_name = config["bundle"]["name"]
        target = config["targets"][self.execution_mode]

        if target["mode"] == "development":
            # For development mode, personalize the job name with username
            user_name = target.get("run_as", {}).get("user_name") or self.client.current_user.me().user_name
            formatted_name = user_name.split("@")[0].replace(".", "_")
            return f"[dev {formatted_name}] {bundle_name}_job"
        return f"{bundle_name}_job"

    def run_job(self) -> Self:
        """
        Execute Databricks job with dynamically generated parameters.

        Looks up the job by name, configures parameters to prevent recursive
        execution, and submits it to Databricks.

        Returns:
            Self: For method chaining

        Raises:
            ValueError: If no job is found with the configured name
        """
        job_name = self.get_job_name()

        # Find the job defined in the Databricks workspace
        job = next(iter(self.client.jobs.list(limit=1, expand_tasks=True, name=job_name)), None)

        if not job:
            logger.error(f"No job found with name: {job_name}")
            raise ValueError(f"No job found with name: {job_name}")

        if job.job_id is None:
            raise ValueError(f"Job {job_name} exists but has no job_id")

        params = self.get_params()

        # Pass parameters to the remote Databricks job, with modifications for proper execution:
        # 1. Disable DAB mode to prevent the job from recursively launching more jobs
        params["dab"] = DabMode.DISABLED.value
        # 2. Use Spark engine since the job runs on a Databricks cluster
        params["query-engine"] = QueryEngine.SPARK.value
        # 3. Disable stdout in the job - results writing will be handled by this process
        params["stdout-mode"] = StdoutMode.DISABLED.value

        logger.info(f"Running job {job_name} (job_id={job.job_id})")
        # Submit the job and wait for it to complete
        run = self.client.jobs.run_now_and_wait(job_id=job.job_id, python_named_params=params)

        # if run.

        logger.info(f"Job {job_name} completed successfully")

        return self

    def entrypoint(self) -> None:
        """
        Entry point determining execution mode (DAB or direct).

        Either executes the query via a separate DAB job or directly
        in the current process. After execution, writes results to stdout
        if enabled.
        """
        if self.dab == DabMode.ENABLED:
            # Execute via a separate Databricks Asset Bundle job
            logger.info("Running in DAB mode via separate Databricks job")
            self.run_job()
        else:
            # Execute directly in the current process (which could be in Databricks)
            logger.info("Running directly in current process (DAB disabled)")
            super().entrypoint()

        # Write results to stdout if enabled
        if self.stdout_mode == StdoutMode.ENABLED:
            logger.info("Writing results to stdout")
            self.write_results_to_stdout()


class AzureIdentityCredentialsStrategy(CredentialsStrategy):
    """
    Authentication strategy using Azure Managed Identity.

    Used in production environments to authenticate with Databricks
    without storing credentials.
    """

    def auth_type(self) -> str:
        """Return the authentication type identifier."""
        return "azure-mi"

    def __init__(self, client_id: str | None = None):
        """
        Initialize with optional client ID.

        Args:
            client_id: Azure Managed Identity client ID
        """
        self.client_id = client_id

    def __call__(self, cfg: "Config") -> CredentialsProvider:
        """
        Create a credentials provider function.

        Args:
            cfg: Databricks configuration

        Returns:
            Function that provides authentication headers
        """
        mi_credential = DefaultAzureCredential(managed_identity_client_id=self.client_id)

        def inner() -> dict[str, str]:
            # Get an Azure AD token for Databricks API
            token = mi_credential.get_token("2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default")
            return {"Authorization": f"Bearer {token.token}"}

        return inner
