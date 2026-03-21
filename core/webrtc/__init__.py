"""WebRTC signaling — re-exported from ``fast_webrtc``. Prefer ``from fast_webrtc import …`` in new code."""

from fast_webrtc import (
    AllowAllMediaConsent,
    BeforeMediaConsentCallback,
    InMemoryRoomRegistry,
    Participant,
    Room,
    SessionExpiredCallback,
    StaticDeniedPeers,
    WebRTCConfiguration,
    WebRTCConfigurationDTO,
    WebRTCSignalingService,
    __version__,
    fetch_twilio_turn_ice_servers,
    ice_servers_from_legacy_webrtc_dto,
    rtc_ice_servers_for_client,
    twilio_tokens_url,
)

__all__ = [
    "AllowAllMediaConsent",
    "BeforeMediaConsentCallback",
    "InMemoryRoomRegistry",
    "Participant",
    "Room",
    "SessionExpiredCallback",
    "StaticDeniedPeers",
    "WebRTCConfiguration",
    "WebRTCConfigurationDTO",
    "WebRTCSignalingService",
    "__version__",
    "fetch_twilio_turn_ice_servers",
    "ice_servers_from_legacy_webrtc_dto",
    "rtc_ice_servers_for_client",
    "twilio_tokens_url",
]
