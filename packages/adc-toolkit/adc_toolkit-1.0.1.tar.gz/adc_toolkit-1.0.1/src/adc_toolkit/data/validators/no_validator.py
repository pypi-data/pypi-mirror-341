"""Validators that do not validate."""

import warnings
from pathlib import Path
from typing import Union

from adc_toolkit.data.abs import Data


class NoValidator:
    """A validator that does not validate the data."""

    def __init__(self) -> None:
        """Initialize the validator."""
        warnings.warn(
            "Not using any validator is not recommended. "
            "Consider using a validator from the `adc_toolkit.data.validators` module.",
            UserWarning,
        )

    @classmethod
    def in_directory(cls, path: Union[str, Path]) -> "NoValidator":
        """Return the validator."""
        return cls()

    def validate(self, name: str, data: Data) -> Data:
        """Return the data without validating it."""
        return data
