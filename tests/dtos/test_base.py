"""Tests for base DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest.mock import patch, MagicMock

import pytest
from pydantic import BaseModel, ValidationError


class TestBaseDTO:
    """Tests for base DTO functionality."""

    def test_create_minimal_dto(self):
        """Test creating minimal DTO."""
        from dtos import BaseDTO
        dto = BaseDTO()
        assert dto is not None

    def test_dto_with_fields(self):
        """Test DTO with fields."""
        from dtos import BaseDTO
        dto = BaseDTO(id="123", name="test")
        assert dto.id == "123"
        assert dto.name == "test"

    def test_dto_to_dict(self):
        """Test DTO to dict conversion."""
        from dtos import BaseDTO
        dto = BaseDTO(id="123", name="test")
        result = dto.to_dict()
        assert result["id"] == "123"
        assert result["name"] == "test"

    def test_dto_to_json(self):
        """Test DTO to JSON conversion."""
        from dtos import BaseDTO
        dto = BaseDTO(id="123", name="test")
        json_str = dto.to_json()
        assert "123" in json_str
        assert "test" in json_str

    def test_dto_from_dict(self):
        """Test DTO from dict creation."""
        from dtos import BaseDTO
        data = {"id": "123", "name": "test"}
        dto = BaseDTO.from_dict(data)
        assert dto.id == "123"
        assert dto.name == "test"

    def test_dto_from_json(self):
        """Test DTO from JSON creation."""
        from dtos import BaseDTO
        json_str = '{"id": "123", "name": "test"}'
        dto = BaseDTO.from_json(json_str)
        assert dto.id == "123"
        assert dto.name == "test"

    def test_dto_copy(self):
        """Test DTO copy."""
        from dtos import BaseDTO
        dto = BaseDTO(id="123", name="test")
        copied = dto.copy()
        assert copied.id == dto.id
        assert copied.name == dto.name

    def test_dto_update(self):
        """Test DTO update."""
        from dtos import BaseDTO
        dto = BaseDTO(id="123", name="test")
        updated = dto.update(name="updated")
        assert updated.id == "123"
        assert updated.name == "updated"


class TestDTOValidation:
    """Tests for DTO validation."""

    def test_required_field_missing(self):
        """Test validation fails for missing required field."""
        from dtos import CreateItemDTO
        with pytest.raises(ValidationError):
            CreateItemDTO()

    def test_required_field_present(self):
        """Test validation passes with required field."""
        from dtos import CreateItemDTO
        dto = CreateItemDTO(name="test")
        assert dto.name == "test"

    def test_string_field_validation(self):
        """Test string field validation."""
        from dtos import CreateItemDTO
        with pytest.raises(ValidationError):
            CreateItemDTO(name=123)  # Should be string

    def test_integer_field_validation(self):
        """Test integer field validation."""
        from dtos import PaginationDTO
        with pytest.raises(ValidationError):
            PaginationDTO(page="not an int")

    def test_enum_field_validation(self):
        """Test enum field validation."""
        from dtos import SortDTO
        with pytest.raises(ValidationError):
            SortDTO(order="invalid_order")

    def test_email_field_validation(self):
        """Test email field validation."""
        from dtos import UserDTO
        with pytest.raises(ValidationError):
            UserDTO(email="not-an-email")

    def test_url_field_validation(self):
        """Test URL field validation."""
        from dtos import LinkDTO
        with pytest.raises(ValidationError):
            LinkDTO(url="not-a-url")

    def test_datetime_field_validation(self):
        """Test datetime field validation."""
        from dtos import EventDTO
        dto = EventDTO(timestamp=datetime.utcnow())
        assert dto.timestamp is not None


class TestDTOOptionalFields:
    """Tests for optional DTO fields."""

    def test_optional_field_not_provided(self):
        """Test optional field can be omitted."""
        from dtos import UpdateItemDTO
        dto = UpdateItemDTO()
        assert dto.name is None

    def test_optional_field_provided(self):
        """Test optional field can be provided."""
        from dtos import UpdateItemDTO
        dto = UpdateItemDTO(name="test")
        assert dto.name == "test"

    def test_optional_field_set_to_none(self):
        """Test optional field can be set to None."""
        from dtos import UpdateItemDTO
        dto = UpdateItemDTO(name=None)
        assert dto.name is None


class TestDTODefaults:
    """Tests for DTO default values."""

    def test_default_value_applied(self):
        """Test default value is applied."""
        from dtos import PaginationDTO
        dto = PaginationDTO()
        assert dto.page == 1
        assert dto.limit == 20

    def test_default_value_overridden(self):
        """Test default value can be overridden."""
        from dtos import PaginationDTO
        dto = PaginationDTO(page=5)
        assert dto.page == 5
        assert dto.limit == 20


class TestDTOInheritance:
    """Tests for DTO inheritance."""

    def test_base_fields_inherited(self):
        """Test base fields are inherited."""
        from dtos import ExtendedItemDTO
        dto = ExtendedItemDTO(id="123", name="test", extra="value")
        assert dto.id == "123"
        assert dto.name == "test"
        assert dto.extra == "value"

    def test_validation_inherited(self):
        """Test validation is inherited."""
        from dtos import ExtendedItemDTO
        with pytest.raises(ValidationError):
            ExtendedItemDTO(name=123)


class TestDTOListsAndNested:
    """Tests for DTOs with lists and nested models."""

    def test_list_field(self):
        """Test list field."""
        from dtos import BulkCreateDTO
        dto = BulkCreateDTO(items=[{"name": "item1"}, {"name": "item2"}])
        assert len(dto.items) == 2

    def test_nested_dto(self):
        """Test nested DTO."""
        from dtos import OrderDTO, AddressDTO
        address = AddressDTO(street="123 Main St", city="Anytown")
        order = OrderDTO(id="123", shipping_address=address)
        assert order.shipping_address.city == "Anytown"

    def test_list_of_nested_dtos(self):
        """Test list of nested DTOs."""
        from dtos import OrderDTO, LineItemDTO
        line_items = [LineItemDTO(name="item1", price=10.0), LineItemDTO(name="item2", price=20.0)]
        order = OrderDTO(id="123", line_items=line_items)
        assert len(order.line_items) == 2


class TestDTOEdgeCases:
    """Test edge cases."""

    def test_empty_string_field(self):
        """Test empty string field."""
        from dtos import CreateItemDTO
        dto = CreateItemDTO(name="")
        assert dto.name == ""

    def test_unicode_field(self):
        """Test unicode field."""
        from dtos import CreateItemDTO
        dto = CreateItemDTO(name="测试项目")
        assert dto.name == "测试项目"

    def test_very_long_string(self):
        """Test very long string field."""
        from dtos import CreateItemDTO
        long_name = "x" * 1000
        dto = CreateItemDTO(name=long_name)
        assert dto.name == long_name

    def test_special_characters(self):
        """Test special characters in field."""
        from dtos import CreateItemDTO
        special = "test<>!@#$%^&*()"
        dto = CreateItemDTO(name=special)
        assert dto.name == special

    def test_whitespace_handling(self):
        """Test whitespace handling."""
        from dtos import CreateItemDTO
        dto = CreateItemDTO(name="  test  ")
        # Whitespace may be stripped or preserved
        assert "test" in dto.name
