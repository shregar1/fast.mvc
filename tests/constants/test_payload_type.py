"""Tests for payload type constants."""

from __future__ import annotations

import pytest

from constants.payload_type import RequestPayloadType, ResponsePayloadType


class TestRequestPayloadType:
    """Tests for RequestPayloadType class."""

    def test_json(self):
        """Test JSON constant."""
        assert RequestPayloadType.JSON == "json"

    def test_form(self):
        """Test FORM constant."""
        assert RequestPayloadType.FORM == "form"

    def test_files(self):
        """Test FILES constant."""
        assert RequestPayloadType.FILES == "files"

    def test_query(self):
        """Test QUERY constant."""
        assert RequestPayloadType.QUERY == "query"


class TestResponsePayloadType:
    """Tests for ResponsePayloadType class."""

    def test_json(self):
        """Test JSON constant."""
        assert ResponsePayloadType.JSON == "json"

    def test_text(self):
        """Test TEXT constant."""
        assert ResponsePayloadType.TEXT == "text"

    def test_content(self):
        """Test CONTENT constant."""
        assert ResponsePayloadType.CONTENT == "content"


class TestRequestPayloadTypeTypes:
    """Tests for request payload type constant types."""

    def test_json_is_string(self):
        """Test JSON is a string."""
        assert isinstance(RequestPayloadType.JSON, str)

    def test_form_is_string(self):
        """Test FORM is a string."""
        assert isinstance(RequestPayloadType.FORM, str)

    def test_files_is_string(self):
        """Test FILES is a string."""
        assert isinstance(RequestPayloadType.FILES, str)

    def test_query_is_string(self):
        """Test QUERY is a string."""
        assert isinstance(RequestPayloadType.QUERY, str)


class TestResponsePayloadTypeTypes:
    """Tests for response payload type constant types."""

    def test_json_is_string(self):
        """Test JSON is a string."""
        assert isinstance(ResponsePayloadType.JSON, str)

    def test_text_is_string(self):
        """Test TEXT is a string."""
        assert isinstance(ResponsePayloadType.TEXT, str)

    def test_content_is_string(self):
        """Test CONTENT is a string."""
        assert isinstance(ResponsePayloadType.CONTENT, str)


class TestRequestPayloadTypeValues:
    """Tests for request payload type constant values."""

    def test_json_is_lowercase(self):
        """Test JSON is lowercase."""
        assert RequestPayloadType.JSON.islower()

    def test_form_is_lowercase(self):
        """Test FORM is lowercase."""
        assert RequestPayloadType.FORM.islower()

    def test_files_is_lowercase(self):
        """Test FILES is lowercase."""
        assert RequestPayloadType.FILES.islower()

    def test_query_is_lowercase(self):
        """Test QUERY is lowercase."""
        assert RequestPayloadType.QUERY.islower()


class TestResponsePayloadTypeValues:
    """Tests for response payload type constant values."""

    def test_json_is_lowercase(self):
        """Test JSON is lowercase."""
        assert ResponsePayloadType.JSON.islower()

    def test_text_is_lowercase(self):
        """Test TEXT is lowercase."""
        assert ResponsePayloadType.TEXT.islower()

    def test_content_is_lowercase(self):
        """Test CONTENT is lowercase."""
        assert ResponsePayloadType.CONTENT.islower()


class TestPayloadTypeUniqueness:
    """Tests for payload type constant uniqueness."""

    def test_all_request_types_unique(self):
        """Test all request payload types are unique."""
        types = [
            RequestPayloadType.JSON,
            RequestPayloadType.FORM,
            RequestPayloadType.FILES,
            RequestPayloadType.QUERY,
        ]
        assert len(types) == len(set(types))

    def test_all_response_types_unique(self):
        """Test all response payload types are unique."""
        types = [
            ResponsePayloadType.JSON,
            ResponsePayloadType.TEXT,
            ResponsePayloadType.CONTENT,
        ]
        assert len(types) == len(set(types))

    def test_json_shared_between_request_and_response(self):
        """Test JSON is shared between request and response types."""
        assert RequestPayloadType.JSON == ResponsePayloadType.JSON
