"""
User Login Request DTO Module.

This module defines the request payload structure for user login.
It includes comprehensive validation for email and password fields
with security checks.

Endpoint: POST /user/login

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


class UserLoginRequestDTO(IRequestDTO, CredentialValidatorMixin, EnhancedBaseModel):
    """
    Request DTO for user login/authentication.

    This DTO validates and sanitizes user login credentials before
    they are processed by the login service. It inherits from both
    IRequestDTO (for reference number) and EnhancedBaseModel (for
    security validation).

    Attributes:
        reference_number (str): Client-provided UUID (from IRequestDTO).
        email (EmailStr): User's email address.
            - Validated for proper email format
            - Normalized (lowercased, trimmed)
        password (str): User's password.
            - Validated for non-empty
            - Validated for password strength requirements

    Validation Rules:
        email and password validators are supplied by
        :class:`~dtos.requests.user.validators.CredentialValidatorMixin`.

    Example:
        >>> from dtos.requests.user.login import UserLoginRequestDTO
        >>>
        >>> login_request = UserLoginRequestDTO(
        ...     reference_number="550e8400-e29b-41d4-a716-446655440000",
        ...     email="User@Example.COM",  # Will be normalized to user@example.com
        ...     password="SecureP@ss123"
        ... )
        >>> login_request.email  # "user@example.com"

    Security:
        - Inherits string sanitization from EnhancedBaseModel
        - Can run validate_security() for injection detection
        - Password is validated but never logged
    """

    email: EmailStr
    """User's email address (validated and normalized)."""

    password: str
    """User's password (validated for strength, never logged)."""
