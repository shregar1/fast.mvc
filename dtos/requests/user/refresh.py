"""
User Refresh Token Request DTO.

Endpoint: POST /user/refresh

Request Body:
    {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
"""

from dtos.base import EnhancedBaseModel
from dtos.requests.abstraction import IRequestDTO


class UserRefreshRequestDTO(IRequestDTO, EnhancedBaseModel):
    """Request DTO for token refresh. Accepts a valid refresh token."""

    refresh_token: str
    """JWT refresh token issued at login."""
