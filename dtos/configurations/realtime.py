"""
DTOs for realtime / collaboration providers.

Covers Pusher, Ably, Supabase Realtime, Socket.IO server, and
generic presence / rooms configuration.
"""

from typing import List, Optional

from pydantic import BaseModel


class PusherConfigDTO(BaseModel):
    enabled: bool = False
    app_id: Optional[str] = None
    key: Optional[str] = None
    secret: Optional[str] = None
    cluster: Optional[str] = None
    use_tls: bool = True


class AblyConfigDTO(BaseModel):
    enabled: bool = False
    api_key: Optional[str] = None


class SupabaseRealtimeConfigDTO(BaseModel):
    enabled: bool = False
    url: Optional[str] = None
    api_key: Optional[str] = None
    default_channels: List[str] = []


class SocketIOServerConfigDTO(BaseModel):
    """
    Configuration for an optional Socket.IO server instance.
    """

    enabled: bool = False
    path: str = "/ws/socket.io"
    cors_origins: List[str] = ["*"]


class PresenceConfigDTO(BaseModel):
    """
    Configuration for the generic presence / rooms service.

    backend can be:
      - "memory": in-process only (default)
      - "redis": use Redis to store membership / presence
    """

    enabled: bool = False
    backend: str = "memory"
    redis_url: Optional[str] = None
    ttl_seconds: int = 60


class RealtimeConfigurationDTO(BaseModel):
    """
    Root DTO aggregating all realtime-related providers.
    """

    pusher: PusherConfigDTO = PusherConfigDTO()
    ably: AblyConfigDTO = AblyConfigDTO()
    supabase: SupabaseRealtimeConfigDTO = SupabaseRealtimeConfigDTO()
    socketio: SocketIOServerConfigDTO = SocketIOServerConfigDTO()
    presence: PresenceConfigDTO = PresenceConfigDTO()

