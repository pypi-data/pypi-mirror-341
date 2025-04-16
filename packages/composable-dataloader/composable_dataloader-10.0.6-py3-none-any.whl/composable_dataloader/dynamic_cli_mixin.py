import typing
from abc import ABC
from dataclasses import is_dataclass
from functools import wraps
from inspect import Parameter, signature
from typing import Annotated, get_origin

import typer

from composable_dataloader.logger import logger


class DynamicCliMixin(ABC):
    """
    Auto-generates CLI interfaces from dataclass annotations.

    This mixin provides functionality to create command-line interfaces dynamically
    based on the fields defined in dataclasses. It extends the approach from
    typer-config to work properly with inheritance hierarchies.

    How it works:
    1. Define fields in dataclasses using `Annotated[type, Option(...)]`
    2. The mixin collects these options across the entire inheritance chain
    3. It then builds a Typer app with these options automatically

    Example:
        ```python
        @dataclass
        class MyLoader(DynamicCliMixin):
            name: Annotated[str, Option("--name", help="The name")]

        # Creates a CLI with --name option automatically
        MyLoader.app()
        ```

    Key features:
    - Child classes inherit CLI options from parent classes
    - Child class definitions override parent options with the same name
    - Handles type conversions and option metadata automatically
    """

    @classmethod
    def get_class_options(cls) -> list[tuple[str, typing.Any]]:
        """
        Extract CLI options (fields using Annotated[Type, Option(...)]) from a dataclass.

        This pattern was inspired by typer-config's approach to configuration management.
        Returns [(name, annotated_type), ...] for each annotated field.
        """
        # Only process actual dataclasses
        if not is_dataclass(cls):
            return []

        options = []
        # Examine each field's type annotation
        for name, field_type in cls.__annotations__.items():
            # Check if it's using Annotated[Type, Option(...)]
            if get_origin(field_type) is Annotated:
                options.append((name, field_type))
        return options

    @classmethod
    def get_cli_options(cls):
        """
        Collect CLI options from the entire inheritance chain.

        This is key to the inheritance behavior - it walks up the class hierarchy
        looking for CLI options in parent classes. Child class definitions
        override parent class definitions for the same option name.

        Returns:
            List of unique (name, annotated_type) tuples
        """
        all_options = []
        seen_names = set()

        # Process the inheritance chain from child to parent (reversed MRO)
        # This ensures child classes override parent options with same name
        for base in reversed(cls.__mro__[:-1]):  # Exclude 'object' class
            if hasattr(base, "get_class_options"):
                for option in base.get_class_options():
                    name = option[0]
                    # Only add if we haven't seen this option name before
                    if name not in seen_names:
                        seen_names.add(name)
                        all_options.append(option)

        return all_options

    @classmethod
    def add_cli_parameters(
        cls, app: typer.Typer, cmd: typing.Callable
    ) -> typing.Callable:
        """
        Dynamically add CLI parameters to a Typer command.

        Modifies a function's signature to include parameters from the class's
        annotated fields, making them available to Typer's CLI generation.

        Args:
            app: Typer app instance
            cmd: Command function to wrap

        Returns:
            Wrapped command function with dynamic parameters
        """
        # Create parameter objects for each CLI option
        new_params = []
        for name, annotated_type in cls.get_cli_options():
            # Extract the original type and the Option object
            type_hint = annotated_type.__origin__
            option = annotated_type.__metadata__[0]  # The Option object

            # Create a new function parameter with the extracted info
            param = Parameter(
                name, kind=Parameter.KEYWORD_ONLY, annotation=type_hint, default=option
            )
            new_params.append(param)

        # Create a wrapper function that preserves metadata (name, docstring, etc.)
        @wraps(cmd)
        def wrapped(**kwargs):
            return cmd(**kwargs)

        # Replace the function's signature with our new parameters
        # This is what makes Typer see the right parameters
        wrapped.__signature__ = signature(cmd).replace(parameters=new_params)

        # Register the function as a Typer command
        return app.command()(wrapped)

    @classmethod
    def app(cls, standalone_mode=True):
        """
        Create a Typer app with auto-generated CLI parameters.

        This is the main entry point for CLI generation. It creates a Typer app,
        defines a main function that creates an instance of the class with the
        provided parameters, and then adds all the CLI parameters to that function.

        Args:
            standalone_mode: Whether Typer should handle exceptions and exit

        Returns:
            Configured Typer app ready to run
        """
        app = typer.Typer(add_completion=False)

        def main(**kwargs):
            """Main CLI entry point with auto-generated options."""
            logger.info(f"Starting {cls.__name__}")

            # Create an instance of the class with the CLI arguments
            instance = cls(**kwargs)

            # Run the instance's entrypoint method
            instance.entrypoint()

        # Add all the CLI parameters to the main function
        cls.add_cli_parameters(app, main)

        # Return the app, possibly executing it immediately if standalone_mode=True
        return app(standalone_mode=standalone_mode)

    def get_params(self) -> dict[str, str]:
        """
        Build parameter dictionary from instance attributes.

        This converts the instance's attributes to a format suitable for
        passing as CLI parameters to other tools or subprocesses.

        Returns:
            Dictionary of parameter name-value pairs in kebab-case format
        """
        params = {}

        # Get all CLI options defined across the class hierarchy
        for name, _ in self.__class__.get_cli_options():
            # Only include attributes that exist and have values
            if hasattr(self, name):
                value = getattr(self, name)
                if value is not None:
                    # Convert snake_case to kebab-case for CLI parameter names
                    param_key = name.replace("_", "-")

                    # Special handling for enum values
                    if hasattr(value, "value"):
                        params[param_key] = value.value
                    else:
                        params[param_key] = str(value)

        return params

    def entrypoint(self) -> None:
        """
        Entry point for CLI execution.

        Default implementation executes the query and writes results.
        Subclasses can override this to customize the execution flow.
        """
        self.execute_and_write()
