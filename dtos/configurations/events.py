"""
Configuration DTOs for cloud event buses and notification services.

Covers:
- AWS SNS (notifications)
- AWS EventBridge (event bus)
- Azure Event Hubs
- Kafka bridge (reuses existing KafkaConfiguration for connectivity)
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class SnsConfigDTO(BaseModel):
    enabled: bool = False
    region: str = "us-east-1"
    topic_arn: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None


class EventBridgeConfigDTO(BaseModel):
    enabled: bool = False
    region: str = "us-east-1"
    bus_name: str = "default"
    source: str = "fastmvc.app"
    detail_type: str = "event"
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None


class EventHubsConfigDTO(BaseModel):
    enabled: bool = False
    connection_string: Optional[str] = None
    event_hub_name: Optional[str] = None


class KafkaBridgeConfigDTO(BaseModel):
    enabled: bool = False
    topic: str = "fastmvc.events"


class EventsConfigurationDTO(BaseModel):
    sns: SnsConfigDTO = SnsConfigDTO()
    event_bridge: EventBridgeConfigDTO = EventBridgeConfigDTO()
    event_hubs: EventHubsConfigDTO = EventHubsConfigDTO()
    kafka: KafkaBridgeConfigDTO = KafkaBridgeConfigDTO()


__all__ = [
    "SnsConfigDTO",
    "EventBridgeConfigDTO",
    "EventHubsConfigDTO",
    "KafkaBridgeConfigDTO",
    "EventsConfigurationDTO",
]

