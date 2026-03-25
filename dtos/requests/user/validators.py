"""
Credential Validator Mixin.

Provides reusable Pydantic field validators for ``email`` and ``password``
fields, shared by ``UserLoginRequestDTO`` and ``UserRegistrationRequestDTO``
to avoid code duplication.

Example:
    >>> class MyDTO(IRequestDTO, CredentialValidatorMixin, EnhancedBaseModel):
    ...     email: EmailStr
    ...     password: str
    ...     # validate_email and validate_password are inherited
"""

from pydantic import EmailStr, field_validator

from fast_utilities.validation import ValidationUtility


class CredentialValidatorMixin:
    """
    Mixin adding ``validate_email`` and ``validate_password`` Pydantic validators.

    Inherit alongside ``BaseModel`` (or a subclass) in any DTO that collects
    user credentials.  The mixin adds no fields of its own — declare ``email``
    and ``password`` on the inheriting class as usual.

    Validators:
        validate_password:
            - Rejects blank / whitespace-only values.
            - Delegates strength checks to :meth:`ValidationUtility.validate_password_strength`.

        validate_email:
            - Validates format via :meth:`ValidationUtility.validate_email_format`.
            - Returns the *normalised* email (lowercase, stripped).

    Example:
        >>> from dtos.requests.user.validators import CredentialValidatorMixin
        >>> from dtos.base import EnhancedBaseModel
        >>> from dtos.requests.abstraction import IRequestDTO
        >>> from pydantic import EmailStr
        >>>
        >>> class MyLoginDTO(IRequestDTO, CredentialValidatorMixin, EnhancedBaseModel):
        ...     email: EmailStr
        ...     password: str
    """

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password is non-empty and meets strength requirements.

        Args:
            v: The password to validate.

        Returns:
            The validated password (unchanged).

        Raises:
            ValueError: If password is empty or fails strength checks.
        """
        if not v or not v.strip():
            raise ValueError("Password cannot be empty.")

        validation_result = ValidationUtility.validate_password_strength(v)
        if not validation_result["is_valid"]:
            issues = ", ".join(validation_result["issues"])
            raise ValueError(f"Password validation failed: {issues}")

        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """
        Validate and normalise an email address.

        Args:
            v: The raw email string.

        Returns:
            The normalised email (lowercased, trimmed).

        Raises:
            ValueError: If the email format is invalid.
        """
        validation_result = ValidationUtility.validate_email_format(v)
        if not validation_result["is_valid"]:
            raise ValueError(f"Invalid email format: {validation_result['error']}")
        return validation_result["normalized_email"]
