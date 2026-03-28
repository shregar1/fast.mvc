"""Exceptions for environment / startup configuration validation."""


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        message = "Configuration validation failed:\n" + "\n".join(
            f"  • {e}" for e in errors
        )
        super().__init__(message)
