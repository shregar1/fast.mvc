"""Tests for HTTP header constants."""

from __future__ import annotations

import pytest

from constants.http_header import HttpHeader


class TestHttpHeader:
    """Tests for HttpHeader class."""

    def test_cache_control(self):
        """Test CACHE_CONTROL header constant."""
        assert HttpHeader.CACHE_CONTROL == "Cache-Control"

    def test_cache_control_value_no_cache(self):
        """Test CACHE_CONTROL_VALUE_NO_CACHE constant."""
        assert HttpHeader.CACHE_CONTROL_VALUE_NO_CACHE == "no-cache"

    def test_x_request_id(self):
        """Test X_REQUEST_ID header constant."""
        assert HttpHeader.X_REQUEST_ID == "X-Request-ID"

    def test_x_process_time(self):
        """Test X_PROCESS_TIME header constant."""
        assert HttpHeader.X_PROCESS_TIME == "X-Process-Time"

    def test_x_reference_urn(self):
        """Test X_REFERENCE_URN header constant."""
        assert HttpHeader.X_REFERENCE_URN == "x-reference-urn"

    def test_x_transaction_urn(self):
        """Test X_TRANSACTION_URN header constant."""
        assert HttpHeader.X_TRANSACTION_URN == "x-transaction-urn"


class TestHttpHeaderTypes:
    """Tests for HTTP header constant types."""

    def test_cache_control_is_string(self):
        """Test CACHE_CONTROL is a string."""
        assert isinstance(HttpHeader.CACHE_CONTROL, str)

    def test_cache_control_value_no_cache_is_string(self):
        """Test CACHE_CONTROL_VALUE_NO_CACHE is a string."""
        assert isinstance(HttpHeader.CACHE_CONTROL_VALUE_NO_CACHE, str)

    def test_x_request_id_is_string(self):
        """Test X_REQUEST_ID is a string."""
        assert isinstance(HttpHeader.X_REQUEST_ID, str)

    def test_x_process_time_is_string(self):
        """Test X_PROCESS_TIME is a string."""
        assert isinstance(HttpHeader.X_PROCESS_TIME, str)

    def test_x_reference_urn_is_string(self):
        """Test X_REFERENCE_URN is a string."""
        assert isinstance(HttpHeader.X_REFERENCE_URN, str)

    def test_x_transaction_urn_is_string(self):
        """Test X_TRANSACTION_URN is a string."""
        assert isinstance(HttpHeader.X_TRANSACTION_URN, str)


class TestGetReferenceUrnHeader:
    """Tests for get_reference_urn_header method."""

    def test_get_reference_urn_header_with_value(self):
        """Test get_reference_urn_header with value."""
        header = HttpHeader()
        result = header.get_reference_urn_header(reference_urn="test-urn")
        assert result == {"x-reference-urn": "test-urn"}

    def test_get_reference_urn_header_with_none(self):
        """Test get_reference_urn_header with None."""
        header = HttpHeader()
        result = header.get_reference_urn_header(reference_urn=None)
        assert result == {}

    def test_get_reference_urn_header_with_empty_string(self):
        """Test get_reference_urn_header with empty string."""
        header = HttpHeader()
        result = header.get_reference_urn_header(reference_urn="")
        assert result == {}

    def test_get_reference_urn_header_no_args(self):
        """Test get_reference_urn_header with no arguments."""
        header = HttpHeader()
        result = header.get_reference_urn_header()
        assert result == {}


class TestCorrelationResponseHeaders:
    """Tests for correlation_response_headers method."""

    def test_correlation_response_headers_with_both(self):
        """Test correlation_response_headers with both URN values."""
        header = HttpHeader()
        result = header.correlation_response_headers(
            reference_urn="ref-urn",
            transaction_urn="txn-urn"
        )
        assert result == {
            "x-reference-urn": "ref-urn",
            "x-transaction-urn": "txn-urn"
        }

    def test_correlation_response_headers_with_reference_only(self):
        """Test correlation_response_headers with reference URN only."""
        header = HttpHeader()
        result = header.correlation_response_headers(reference_urn="ref-urn")
        assert result == {"x-reference-urn": "ref-urn"}

    def test_correlation_response_headers_with_transaction_only(self):
        """Test correlation_response_headers with transaction URN only."""
        header = HttpHeader()
        result = header.correlation_response_headers(transaction_urn="txn-urn")
        assert result == {"x-transaction-urn": "txn-urn"}

    def test_correlation_response_headers_with_none(self):
        """Test correlation_response_headers with None values."""
        header = HttpHeader()
        result = header.correlation_response_headers(
            reference_urn=None,
            transaction_urn=None
        )
        assert result == {}

    def test_correlation_response_headers_with_empty_strings(self):
        """Test correlation_response_headers with empty string values."""
        header = HttpHeader()
        result = header.correlation_response_headers(
            reference_urn="",
            transaction_urn=""
        )
        assert result == {}

    def test_correlation_response_headers_no_args(self):
        """Test correlation_response_headers with no arguments."""
        header = HttpHeader()
        result = header.correlation_response_headers()
        assert result == {}

    def test_correlation_response_headers_empty_reference_valid_transaction(self):
        """Test correlation_response_headers with empty reference and valid transaction."""
        header = HttpHeader()
        result = header.correlation_response_headers(
            reference_urn="",
            transaction_urn="txn-urn"
        )
        assert result == {"x-transaction-urn": "txn-urn"}
