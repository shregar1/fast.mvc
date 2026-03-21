"""
Template packs for `fastmvc generate` / `fastmvc init`.

``standard`` matches historical CLI defaults. ``minimal`` trims integrations;
``full`` enables common production-oriented options.
"""

from __future__ import annotations

from typing import Any


def apply_template_pack(generator: Any, pack: str) -> None:
    """
    Override generator flags after CLI / wizard options.

    Used when the user selects a non-standard template pack and confirms
    that presets should win over earlier answers.
    """
    p = (pack or "standard").lower()
    if p == "standard":
        return

    if p == "minimal":
        generator.use_redis = False
        generator.use_mongo = False
        generator.use_cassandra = False
        generator.use_scylla = False
        generator.use_dynamo = False
        generator.use_cosmos = False
        generator.use_elasticsearch = False
        generator.use_neo4j = False
        generator.use_meilisearch = False
        generator.use_typesense = False
        generator.use_email = False
        generator.use_slack = False
        generator.use_datadog = False
        generator.use_telemetry = False
        generator.use_payments = False
        generator.use_rabbitmq = False
        generator.use_sqs = False
        generator.use_service_bus = False
        generator.use_celery = False
        generator.use_analytics = False
        generator.use_events = False
        generator.use_vault = False
        generator.use_aws_secrets = False
        generator.use_feature_flags = False
        generator.use_s3 = False
        generator.use_gcs = False
        generator.use_azure_blob = False
        generator.use_llm = False
        generator.use_pinecone = False
        generator.use_qdrant = False
        generator.use_streams = False
        generator.use_identity = False
        generator.enable_auth = False
        generator.enable_user_mgmt = False
        generator.enable_product_crud = False
        generator.api_preset = "crud"
        generator.include_docker_compose = False
        return

    if p == "full":
        generator.use_redis = True
        generator.use_rabbitmq = True
        generator.use_celery = True
        generator.use_identity = True
        generator.use_analytics = True
        generator.use_events = True
        generator.use_s3 = True
        generator.use_vault = True
        generator.use_feature_flags = True
        generator.use_payments = True
        generator.use_email = True
        generator.use_datadog = False
        generator.use_telemetry = True
        generator.enable_auth = True
        generator.enable_user_mgmt = True
        generator.enable_product_crud = True
        generator.api_preset = "admin"
        generator.include_docker_compose = True
        return

    raise ValueError(f"Unknown template pack: {pack!r}")
