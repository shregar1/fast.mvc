"""Tests for filter operator constants."""

from __future__ import annotations

import pytest

from constants.filter_operator import FilterOperator


class TestFilterOperator:
    """Tests for FilterOperator class."""

    def test_eq(self):
        """Test EQ constant."""
        assert FilterOperator.EQ == "eq"

    def test_ne(self):
        """Test NE constant."""
        assert FilterOperator.NE == "ne"

    def test_lt(self):
        """Test LT constant."""
        assert FilterOperator.LT == "lt"

    def test_le(self):
        """Test LE constant."""
        assert FilterOperator.LE == "le"

    def test_gt(self):
        """Test GT constant."""
        assert FilterOperator.GT == "gt"

    def test_ge(self):
        """Test GE constant."""
        assert FilterOperator.GE == "ge"

    def test_gte_alias(self):
        """Test GTE is alias for GE."""
        assert FilterOperator.GTE == FilterOperator.GE

    def test_lte_alias(self):
        """Test LTE is alias for LE."""
        assert FilterOperator.LTE == FilterOperator.LE

    def test_in(self):
        """Test IN constant."""
        assert FilterOperator.IN == "in"

    def test_not_in(self):
        """Test NOT_IN constant."""
        assert FilterOperator.NOT_IN == "not_in"

    def test_like(self):
        """Test LIKE constant."""
        assert FilterOperator.LIKE == "like"

    def test_ilike(self):
        """Test ILIKE constant."""
        assert FilterOperator.ILIKE == "ilike"

    def test_is_null(self):
        """Test IS_NULL constant."""
        assert FilterOperator.IS_NULL == "is_null"

    def test_is_not_null(self):
        """Test IS_NOT_NULL constant."""
        assert FilterOperator.IS_NOT_NULL == "is_not_null"

    def test_between(self):
        """Test BETWEEN constant."""
        assert FilterOperator.BETWEEN == "between"


class TestFilterOperatorTypes:
    """Tests for filter operator constant types."""

    def test_eq_is_string(self):
        """Test EQ is a string."""
        assert isinstance(FilterOperator.EQ, str)

    def test_ne_is_string(self):
        """Test NE is a string."""
        assert isinstance(FilterOperator.NE, str)

    def test_lt_is_string(self):
        """Test LT is a string."""
        assert isinstance(FilterOperator.LT, str)

    def test_le_is_string(self):
        """Test LE is a string."""
        assert isinstance(FilterOperator.LE, str)

    def test_gt_is_string(self):
        """Test GT is a string."""
        assert isinstance(FilterOperator.GT, str)

    def test_ge_is_string(self):
        """Test GE is a string."""
        assert isinstance(FilterOperator.GE, str)

    def test_in_is_string(self):
        """Test IN is a string."""
        assert isinstance(FilterOperator.IN, str)

    def test_not_in_is_string(self):
        """Test NOT_IN is a string."""
        assert isinstance(FilterOperator.NOT_IN, str)

    def test_like_is_string(self):
        """Test LIKE is a string."""
        assert isinstance(FilterOperator.LIKE, str)

    def test_ilike_is_string(self):
        """Test ILIKE is a string."""
        assert isinstance(FilterOperator.ILIKE, str)

    def test_is_null_is_string(self):
        """Test IS_NULL is a string."""
        assert isinstance(FilterOperator.IS_NULL, str)

    def test_is_not_null_is_string(self):
        """Test IS_NOT_NULL is a string."""
        assert isinstance(FilterOperator.IS_NOT_NULL, str)

    def test_between_is_string(self):
        """Test BETWEEN is a string."""
        assert isinstance(FilterOperator.BETWEEN, str)


class TestFilterOperatorValues:
    """Tests for filter operator constant values."""

    def test_eq_is_lowercase(self):
        """Test EQ is lowercase."""
        assert FilterOperator.EQ.islower()

    def test_ne_is_lowercase(self):
        """Test NE is lowercase."""
        assert FilterOperator.NE.islower()

    def test_lt_is_lowercase(self):
        """Test LT is lowercase."""
        assert FilterOperator.LT.islower()

    def test_le_is_lowercase(self):
        """Test LE is lowercase."""
        assert FilterOperator.LE.islower()

    def test_gt_is_lowercase(self):
        """Test GT is lowercase."""
        assert FilterOperator.GT.islower()

    def test_ge_is_lowercase(self):
        """Test GE is lowercase."""
        assert FilterOperator.GE.islower()

    def test_in_is_lowercase(self):
        """Test IN is lowercase."""
        assert FilterOperator.IN.islower()

    def test_not_in_contains_underscore(self):
        """Test NOT_IN contains underscore."""
        assert "_" in FilterOperator.NOT_IN

    def test_is_null_contains_underscore(self):
        """Test IS_NULL contains underscore."""
        assert "_" in FilterOperator.IS_NULL

    def test_is_not_null_contains_underscore(self):
        """Test IS_NOT_NULL contains underscore."""
        assert "_" in FilterOperator.IS_NOT_NULL
