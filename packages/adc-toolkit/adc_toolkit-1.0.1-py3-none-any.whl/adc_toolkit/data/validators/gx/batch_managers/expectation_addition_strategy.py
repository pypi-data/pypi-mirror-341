"""
Expectation addition strategy.

This module contains expectation strategies.
Depending on the strategy, different expectations will be added to the expectation suite.
"""

from typing import Protocol

from adc_toolkit.data.validators.gx.batch_managers.batch_manager import BatchManager
from adc_toolkit.data.validators.gx.batch_managers.expectation_addition import ValidatorBasedExpectationAddition
from adc_toolkit.data.validators.gx.custom_expectations.expect_batch_schema_to_match_dict import (  # noqa
    ExpectBatchSchemaToMatchDict,
)
from adc_toolkit.data.validators.table_utils.table_properties import extract_dataframe_schema


class ExpectationAdditionStrategy(Protocol):
    """Expectation addition strategy."""

    def add_expectations(self, batch_manager: BatchManager) -> None:
        """Add expectations."""
        ...


class SkipExpectationAddition:
    """
    Skip adding expectations.

    This class skips adding expectations. It is used when the expectation suite already exists
    and filled with expectations.
    """

    def add_expectations(self, batch_manager: BatchManager) -> None:
        """Skip creating expectations."""


class SchemaExpectationAddition:
    """
    Schema expectation addition strategy.

    This class adds schema expectations to the expectation suite.
    Schema expectations are expectations that check the schema of the data:
    the column names and the column types.
    """

    def _check_if_expectation_exists(self, batch_manager: BatchManager) -> bool:
        """
        Check if the expectation already exists in the suite.

        This method checks if the schema expectation already exists in the suite.

        Returns
        -------
        bool
            True if the expectation already exists in the suite, False otherwise.
        """
        suite = batch_manager.data_context.get_expectation_suite(expectation_suite_name=f"{batch_manager.name}_suite")
        return len(suite.expectations) > 0

    def add_expectations(self, batch_manager: BatchManager) -> None:
        """
        Add schema expectations to the expectation suite.

        This method adds schema expectations to the expectation suite.
        It freezes the dataframe schema by creating an expectation suite
        out of the dataframe schema. "Freezing" the dataframe schema means that
        the validator will fix the column list and the column types of the dataframe.
        Next time the data is validated, the validator will expect the dataframe
        to have the same schema.

        Returns
        -------
        None
        """
        if not self._check_if_expectation_exists(batch_manager):
            ValidatorBasedExpectationAddition().add_expectations(
                batch_manager,
                expectations=[
                    {"expect_batch_schema_to_match_dict": {"schema": extract_dataframe_schema(batch_manager.data)}}
                ],
            )
