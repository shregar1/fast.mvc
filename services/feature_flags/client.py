"""
Feature flag client abstraction.

Supports LaunchDarkly and Unleash via a minimal ``IFeatureFlagClient``
interface, wired from configuration.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from loguru import logger

from configurations.feature_flags import FeatureFlagsConfiguration

try:  # Optional dependencies
    import httpx
except Exception:  # pragma: no cover - optional
    httpx = None  # type: ignore

try:
    import ldclient
    from ldclient.config import Config as LDConfig
except Exception:  # pragma: no cover - optional
    ldclient = None  # type: ignore
    LDConfig = None  # type: ignore


class IFeatureFlagClient(ABC):
    @abstractmethod
    async def is_enabled(self, key: str, user: Dict[str, Any] | None = None, default: bool = False) -> bool:  # pragma: no cover - interface
        raise NotImplementedError


class LaunchDarklyClient(IFeatureFlagClient):
    def __init__(self, sdk_key: str, default_user_key: str) -> None:
        if ldclient is None or LDConfig is None:  # pragma: no cover - optional
            raise RuntimeError("launchdarkly-server-sdk is not installed")
        ldclient.set_config(LDConfig(sdk_key=sdk_key))
        self._client = ldclient.get()
        self._default_user_key = default_user_key

    async def is_enabled(self, key: str, user: Dict[str, Any] | None = None, default: bool = False) -> bool:
        u = user or {"key": self._default_user_key}
        return bool(self._client.variation(key, u, default))


class UnleashClient(IFeatureFlagClient):
    def __init__(self, url: str, app_name: str, instance_id: str, api_key: str | None) -> None:
        if httpx is None:  # pragma: no cover - optional
            raise RuntimeError("httpx is not installed")
        self._url = url.rstrip("/")
        self._app_name = app_name
        self._instance_id = instance_id
        self._api_key = api_key

    async def is_enabled(self, key: str, user: Dict[str, Any] | None = None, default: bool = False) -> bool:
        headers = {
            "Content-Type": "application/json",
            "UNLEASH-APPNAME": self._app_name,
            "UNLEASH-INSTANCEID": self._instance_id,
        }
        if self._api_key:
            headers["Authorization"] = self._api_key

        payload = {
            "userId": user.get("key") if user else None,
            "properties": user or {},
        }

        url = f"{self._url}/client/features/{key}/evaluate"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=payload, headers=headers, timeout=3)
                if resp.status_code >= 400:
                    logger.warning("Unleash evaluation error %s: %s", resp.status_code, resp.text)
                    return default
                data = resp.json()
                return bool(data.get("enabled", default))
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Unleash evaluation failure for %s: %s", key, exc)
                return default


def build_feature_flag_client() -> IFeatureFlagClient | None:
    """
    Build a feature flag client from configuration.

    Priority:
      - LaunchDarkly
      - Unleash
    """

    cfg = FeatureFlagsConfiguration.instance().get_config()

    if cfg.launchdarkly.enabled and cfg.launchdarkly.sdk_key:
        try:
            return LaunchDarklyClient(
                sdk_key=cfg.launchdarkly.sdk_key,
                default_user_key=cfg.launchdarkly.default_user_key,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize LaunchDarkly client: %s", exc)

    if cfg.unleash.enabled:
        try:
            return UnleashClient(
                url=cfg.unleash.url,
                app_name=cfg.unleash.app_name,
                instance_id=cfg.unleash.instance_id,
                api_key=cfg.unleash.api_key,
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to initialize Unleash client: %s", exc)

    logger.info("No feature flag provider is enabled.")
    return None


__all__ = [
    "IFeatureFlagClient",
    "LaunchDarklyClient",
    "UnleashClient",
    "build_feature_flag_client",
]

