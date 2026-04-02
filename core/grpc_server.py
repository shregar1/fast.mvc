"""Optional gRPC server support (health-first).

This keeps gRPC as an opt-in transport, aligned with FastMVC's configuration
and layered approach.

Currently implemented:
- gRPC server with a simple unary HealthService.Check RPC.

Future expansion:
- Add more gRPC services as separate vertical-slice modules.
- Reuse the same JWT auth configuration for gRPC interceptors.
"""

from __future__ import annotations

import time
from collections.abc import Iterable
from typing import Any, Callable, Optional

from loguru import logger

from constants.default import Default
from constants.environment import EnvironmentVar
from utilities.env import EnvironmentParserUtility


def _build_health_messages():
    """Create protobuf message classes + wire a minimal service descriptor."""
    # Local imports to avoid importing grpc when GRPC_ENABLED=false.
    import grpc  # type: ignore
    from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

    package = "fastmvc.grpc.health.v1"
    file_name = "fastmvc/grpc/health/v1/health.proto"

    file_proto = descriptor_pb2.FileDescriptorProto()
    file_proto.name = file_name
    file_proto.package = package
    file_proto.syntax = "proto3"

    # HealthRequest { string service = 1; }
    msg_req = file_proto.message_type.add()
    msg_req.name = "HealthRequest"
    field_service = msg_req.field.add()
    field_service.name = "service"
    field_service.number = 1
    field_service.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    field_service.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    # HealthResponse { string status = 1; int64 timestamp_unix_ms = 2; string details = 3; }
    msg_resp = file_proto.message_type.add()
    msg_resp.name = "HealthResponse"
    f_status = msg_resp.field.add()
    f_status.name = "status"
    f_status.number = 1
    f_status.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    f_status.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    f_ts = msg_resp.field.add()
    f_ts.name = "timestamp_unix_ms"
    f_ts.number = 2
    f_ts.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    f_ts.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT64

    f_details = msg_resp.field.add()
    f_details.name = "details"
    f_details.number = 3
    f_details.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    f_details.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    # service HealthService { rpc Check(HealthRequest) returns (HealthResponse); }
    svc = file_proto.service.add()
    svc.name = "HealthService"
    method = svc.method.add()
    method.name = "Check"
    method.input_type = f".{package}.HealthRequest"
    method.output_type = f".{package}.HealthResponse"

    pool = descriptor_pool.DescriptorPool()
    pool.Add(file_proto)
    # Avoid deprecated MessageFactory usage (protobuf >= 4.23).
    HealthRequest = message_factory.GetMessageClass(
        pool.FindMessageTypeByName(f"{package}.HealthRequest")
    )
    HealthResponse = message_factory.GetMessageClass(
        pool.FindMessageTypeByName(f"{package}.HealthResponse")
    )

    service_full_name = f"{package}.HealthService"
    method_name = "Check"
    return grpc, HealthRequest, HealthResponse, service_full_name, method_name


def _extract_bearer_token(metadata: Iterable[tuple[str, Any]]) -> Optional[str]:
    for k, v in metadata:
        if str(k).lower() == "authorization" and v is not None:
            s = str(v)
            if s.lower().startswith("bearer "):
                return s.split(" ", 1)[1].strip()
    return None


async def start_grpc_health_server() -> Any:
    """Start the optional gRPC health server and return the aio server."""
    # Local imports so FastMVC works without grpc installed (until enabled).
    import grpc  # type: ignore

    grpc_mod, HealthRequest, HealthResponse, service_full_name, method_name = _build_health_messages()

    jwt_enabled = EnvironmentParserUtility.get_bool_with_logging(
        EnvironmentVar.JWT_AUTH_ENABLED,
        Default.JWT_AUTH_ENABLED,
    )
    jwt_secret = EnvironmentParserUtility.parse_str(
        EnvironmentVar.SECRET_KEY,
        Default.SECRET_KEY,
    )
    jwt_algorithm = EnvironmentParserUtility.parse_str(
        EnvironmentVar.ALGORITHM,
        Default.ALGORITHM,
    )

    host = EnvironmentParserUtility.parse_str(EnvironmentVar.GRPC_HOST, Default.GRPC_HOST)
    port = EnvironmentParserUtility.parse_int(EnvironmentVar.GRPC_PORT, Default.GRPC_PORT)

    # Match FastAPI behavior: if JWT is enabled but secret isn't configured,
    # HTTP middleware is not registered. For gRPC, we also skip enforcement.
    jwt_enabled_effective = bool(jwt_enabled and jwt_secret.strip())
    if jwt_enabled and not jwt_secret.strip():
        logger.warning(
            "JWT_AUTH_ENABLED is true but SECRET_KEY is empty; gRPC JWT enforcement disabled."
        )

    jwt_decode: Optional[Callable[..., Any]] = None
    if jwt_enabled_effective:
        import jwt as _jwt  # pyjwt

        jwt_decode = _jwt.decode

    server = grpc_mod.aio.server()

    async def check(request, context) -> Any:  # request/response are dynamic protobuf messages
        if jwt_enabled_effective:
            # Keep behavior consistent with REST auth: require Bearer token when JWT is enabled.
            token = _extract_bearer_token(context.invocation_metadata())
            if not token:
                await context.abort(
                    grpc_mod.StatusCode.UNAUTHENTICATED, "Missing Bearer token"
                )
                return HealthResponse(
                    status="ERROR", timestamp_unix_ms=0, details="Missing Bearer token"
                )

            try:
                assert jwt_decode is not None  # for type checkers
                jwt_decode(token, jwt_secret, algorithms=[jwt_algorithm])
            except Exception:
                await context.abort(grpc_mod.StatusCode.UNAUTHENTICATED, "Invalid token")
                return HealthResponse(
                    status="ERROR", timestamp_unix_ms=0, details="Invalid token"
                )

        return HealthResponse(
            status="SERVING",
            timestamp_unix_ms=int(time.time() * 1000),
            details="gRPC health ok",
        )

    request_deserializer = lambda b: HealthRequest.FromString(b)
    response_serializer = lambda m: m.SerializeToString()

    handler = grpc_mod.unary_unary_rpc_method_handler(
        check,
        request_deserializer=request_deserializer,
        response_serializer=response_serializer,
    )
    generic_handler = grpc_mod.method_handlers_generic_handler(
        service_full_name,
        {method_name: handler},
    )
    server.add_generic_rpc_handlers((generic_handler,))

    bound_port = server.add_insecure_port(f"{host}:{port}")
    setattr(server, "_fastmvc_bound_port", bound_port)

    await server.start()
    logger.info(f"gRPC HealthService started on {host}:{bound_port}")
    return server


async def stop_grpc_server(server: Any, grace_seconds: int = 5) -> None:
    """Gracefully stop the aio gRPC server."""
    if server is None:
        return
    try:
        await server.stop(grace_seconds)
    except Exception:
        # Best-effort shutdown; don't crash app shutdown.
        logger.exception("Failed to stop gRPC server cleanly")

