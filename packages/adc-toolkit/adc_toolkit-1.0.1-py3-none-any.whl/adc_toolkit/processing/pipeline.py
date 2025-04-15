"""Module with a pipeline for data processing."""

import copy
from typing import Any, Callable

from ..data.abs import Data
from ..logger import Logger
from .step import PipelineStep

logger = Logger()


class ProcessingPipeline:
    """A pipeline for processing data."""

    def __init__(self) -> None:
        """Initialize the processing pipeline."""
        self.steps = list[PipelineStep]()

    def __str__(self) -> str:
        """Return a string representation of the processing pipeline."""
        return " -> ".join([str(step) for step in self.steps])

    def __len__(self) -> int:
        """Return the number of steps in the pipeline."""
        return len(self.steps)

    def add(
        self,
        step: Callable[..., Data],
        **kwargs: Any,
    ) -> "ProcessingPipeline":
        """
        Add a step to the pipeline.

        Parameters
        ----------
        step : Callable[..., Data]
            The function to execute.
        kwargs : Any
            The keyword arguments to pass to the step.

        Returns
        -------
        ProcessingPipeline
            The updated processing pipeline.
        """
        self.steps.append(PipelineStep(step, **kwargs))

        return self

    def run(self, data: Data) -> Data:
        """Run the processing pipeline.

        Parameters
        ----------
        data : Data
            The data to process.

        Returns
        -------
        Data
            The processed data.
        """
        # logger.info(f"Running pipeline with {len(self)} steps.")

        result = copy.deepcopy(data)

        for step in self.steps:
            result = step.execute(result)

        # logger.info("Pipeline finished successfully.")

        return result
