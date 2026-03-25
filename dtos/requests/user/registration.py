"""
User Registration Request DTO Module.

This module defines the request payload structure for new user registration.
It includes comprehensive validation for email and password fields
with security checks.

Endpoint: POST /user/register

Request Body:
    {
        "reference_number": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "password": "SecureP@ss123"
    }
"""

from pydantic import EmailStr

from dtos.base import EnhancedBaseModel
from dtos.requests.abstraction import IRequestDTO
from dtos.requests.user.validators import CredentialValidatorMixin


class UserRegistrationRequestDTO(IRequestDTO, CredentialValidatorMixin, EnhancedBaseModel):
    """
    Request DTO for new user registration.

    This DTO validates and sanitizes user registration data before
    a new account is created. It inherits from both IRequestDTO
    (for reference number) and EnhancedBaseModel (for security validation).

    Attributes:
        reference_number (str): Client-provided UUID (from IRequestDTO).
        email (EmailStr): User's email address for the new account.
            - Validated for proper email format
            - Normalized (lowercased, trimmed)
            - Must be unique (checked by service layer)
        password (str): Password for the new account.
            - Validated for non-empty
            - Validated for password strength requirements

    Validation Rules:
        email and password validators are supplied by
        :class:`~dtos.requests.user.validators.CredentialValidatorMixin`.

    Example:
        >>> from dtos.requests.user.registration import UserRegistrationRequestDTO
        >>>
        >>> registration = UserRegistrationRequestDTO(
        ...     reference_number="550e8400-e29b-41d4-a716-446655440000",
        ...     email="NewUser@Example.COM",
        ...     password="MySecure@Pass1"
        ... )
        >>> registration.email  # "newuser@example.com"

    Security:
        - Inherits string sanitization from EnhancedBaseModel
        - Can run validate_security() for injection detection
        - Password is hashed before storage (in service layer)
    """

    email: EmailStr
    """Email address for the new account (validated and normalized)."""

    password: str
    """Password for the new account (validated, will be hashed)."""
