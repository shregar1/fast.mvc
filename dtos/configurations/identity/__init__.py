"""
Identity providers / SSO configuration DTOs.

Supports OAuth2/OIDC providers (Google, GitHub, Azure AD, Okta, Auth0)
and SAML SSO for enterprise identity.
"""

from pydantic import BaseModel
from typing import Literal, Optional


class OAuth2ProviderConfigDTO(BaseModel):
    """
    Base OAuth2/OIDC provider configuration.
    """

    enabled: bool = False
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    auth_url: Optional[str] = None
    token_url: Optional[str] = None
    userinfo_url: Optional[str] = None
    scopes: list[str] = []


class GoogleConfigDTO(OAuth2ProviderConfigDTO):
    """Google OAuth2/OIDC configuration."""


class GitHubConfigDTO(OAuth2ProviderConfigDTO):
    """GitHub OAuth2 configuration."""


class AzureADConfigDTO(OAuth2ProviderConfigDTO):
    """Azure AD OAuth2/OIDC configuration."""


class OktaConfigDTO(OAuth2ProviderConfigDTO):
    """Okta OAuth2/OIDC configuration."""


class Auth0ConfigDTO(OAuth2ProviderConfigDTO):
    """Auth0 OAuth2/OIDC configuration."""


class SAMLProviderConfigDTO(BaseModel):
    """
    SAML SSO configuration.

    In production, this would include certificates, metadata URLs,
    ACS URLs, entity IDs, etc.
    """

    enabled: bool = False
    idp_metadata_url: Optional[str] = None
    sp_entity_id: Optional[str] = None
    acs_url: Optional[str] = None


class IdentityProvidersConfigurationDTO(BaseModel):
    """
    Aggregated configuration for all identity providers.
    """

    google: GoogleConfigDTO = GoogleConfigDTO()
    github: GitHubConfigDTO = GitHubConfigDTO()
    azure_ad: AzureADConfigDTO = AzureADConfigDTO()
    okta: OktaConfigDTO = OktaConfigDTO()
    auth0: Auth0ConfigDTO = Auth0ConfigDTO()
    saml: SAMLProviderConfigDTO = SAMLProviderConfigDTO()


__all__ = [
    "OAuth2ProviderConfigDTO",
    "GoogleConfigDTO",
    "GitHubConfigDTO",
    "AzureADConfigDTO",
    "OktaConfigDTO",
    "Auth0ConfigDTO",
    "SAMLProviderConfigDTO",
    "IdentityProvidersConfigurationDTO",
]

