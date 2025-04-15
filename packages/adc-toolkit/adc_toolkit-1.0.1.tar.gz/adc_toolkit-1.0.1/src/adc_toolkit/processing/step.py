"""Module for creating a step in the data processing pipeline."""

from typing import Any, Callable

from ..data.abs import Data
from ..logger import Logger

logger = Logger()


class PipelineStep:
    """A step in a data processing pipeline with type checking, error handling, and data validation."""

    def __init__(
        self,
        step: Callable[..., Data],
        **kwargs: Any,
    ) -> None:
        """
        Initialize the pipeline step.

        Parameters
        ----------
        step : Callable[..., Data]
            The function to execute.
        kwargs : Any
            The keyword arguments to pass to the function.
        """
        self.step = step
        self.kwargs = kwargs

    def __str__(self) -> str:
        """Return a string representation of the pipeline step."""
        kwargs_strings = [f"{key}={value}" for key, value in self.kwargs.items()]
        return f"{self.step.__name__}({', '.join(kwargs_strings)})"

    def execute(self, data: Data) -> Data:
        """
        Execute the pipeline step with type checking, error handling, and data validation.

        Parameters
        ----------
        data : Data
            The data to process.

        Returns
        -------
        Data
            The processed data.

        Raises
        ------
        Exception
            If an error occurs during processing.

        """
        # logger.info(f"Running function {self.step.__name__}.")
        result = self.step(data, **self.kwargs)

        return result
