import time

import pytest

import grpc

from fastx.grpc.health.v1 import health_pb2, health_pb2_grpc
from fastx.grpc.user.v1 import user_pb2, user_pb2_grpc


@pytest.mark.asyncio
async def test_grpc_health_serving_without_jwt(monkeypatch):
    """When JWT is disabled, HealthService.Check returns SERVING."""
    monkeypatch.setenv("GRPC_ENABLED", "true")
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")  # ephemeral port
    monkeypatch.setenv("JWT_AUTH_ENABLED", "false")
    monkeypatch.setenv("SECRET_KEY", "")
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")
    assert bound_port != 0

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = health_pb2_grpc.HealthServiceStub(channel)
        resp = await stub.Check(health_pb2.HealthRequest(service=""), timeout=2.0)
        assert resp.status == "SERVING"
    finally:
        await stop_grpc_server(server)


@pytest.mark.asyncio
async def test_grpc_health_jwt_enabled_secret_missing_allows_like_http(monkeypatch):
    """Match FastX HTTP behavior: if JWT enabled but SECRET_KEY empty, enforcement is disabled."""
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")
    monkeypatch.setenv("JWT_AUTH_ENABLED", "true")
    monkeypatch.setenv("SECRET_KEY", "")  # enforcement disabled in core/grpc_server
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = health_pb2_grpc.HealthServiceStub(channel)
        resp = await stub.Check(health_pb2.HealthRequest(service=""), timeout=2.0)
        assert resp.status == "SERVING"
    finally:
        await stop_grpc_server(server)


@pytest.mark.asyncio
async def test_grpc_health_jwt_enabled_requires_bearer_token(monkeypatch):
    """When JWT is enabled and SECRET_KEY configured, missing token returns UNAUTHENTICATED."""
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")
    monkeypatch.setenv("JWT_AUTH_ENABLED", "true")
    monkeypatch.setenv("SECRET_KEY", "a_very_long_and_complex_secret_key!")
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = health_pb2_grpc.HealthServiceStub(channel)

        with pytest.raises(grpc.RpcError) as excinfo:
            await stub.Check(health_pb2.HealthRequest(service=""), timeout=2.0)

        # grpc.aio exceptions expose grpc_status_code via details/code properties.
        assert excinfo.value.code().name == "UNAUTHENTICATED"
    finally:
        await stop_grpc_server(server)


@pytest.mark.asyncio
async def test_grpc_health_jwt_enabled_accepts_valid_bearer_token(monkeypatch):
    """A valid bearer token allows HealthService.Check to succeed."""
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")
    monkeypatch.setenv("JWT_AUTH_ENABLED", "true")
    monkeypatch.setenv("SECRET_KEY", "a_very_long_and_complex_secret_key!")
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    import jwt as pyjwt

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = health_pb2_grpc.HealthServiceStub(channel)

        payload = {"sub": "user-1", "exp": int(time.time()) + 60}
        token = pyjwt.encode(payload, "a_very_long_and_complex_secret_key!", algorithm="HS256")

        resp = await stub.Check(
            health_pb2.HealthRequest(service=""),
            metadata=[("authorization", f"Bearer {token}")],
            timeout=2.0,
        )
        assert resp.status == "SERVING"
    finally:
        await stop_grpc_server(server)


@pytest.mark.asyncio
async def test_grpc_fetch_user_serving_without_jwt(monkeypatch):
    """When JWT is disabled, FetchUser returns expected payload."""
    monkeypatch.setenv("GRPC_ENABLED", "true")
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")  # ephemeral port
    monkeypatch.setenv("JWT_AUTH_ENABLED", "false")
    monkeypatch.setenv("SECRET_KEY", "")
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = user_pb2_grpc.UserServiceStub(channel)

        resp = await stub.FetchUser(
            user_pb2.FetchUserRequest(name="alice", description="dev"),
            timeout=2.0,
        )
        assert resp.id == "1"
        assert resp.message == "Success"
        assert resp.status == "active"
    finally:
        await stop_grpc_server(server)


@pytest.mark.asyncio
async def test_grpc_fetch_user_jwt_enabled_requires_bearer_token(monkeypatch):
    """When JWT is enabled and SECRET_KEY configured, missing token returns UNAUTHENTICATED."""
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")
    monkeypatch.setenv("JWT_AUTH_ENABLED", "true")
    monkeypatch.setenv("SECRET_KEY", "a_very_long_and_complex_secret_key!")
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = user_pb2_grpc.UserServiceStub(channel)

        with pytest.raises(grpc.RpcError) as excinfo:
            await stub.FetchUser(
                user_pb2.FetchUserRequest(name="alice", description="dev"),
                timeout=2.0,
            )

        assert excinfo.value.code().name == "UNAUTHENTICATED"
    finally:
        await stop_grpc_server(server)


@pytest.mark.asyncio
async def test_grpc_fetch_user_jwt_enabled_accepts_valid_bearer_token(monkeypatch):
    """A valid bearer token allows FetchUser to succeed."""
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "0")
    monkeypatch.setenv("JWT_AUTH_ENABLED", "true")
    monkeypatch.setenv("SECRET_KEY", "a_very_long_and_complex_secret_key!")
    monkeypatch.setenv("ALGORITHM", "HS256")

    from core.grpc_server import start_grpc_health_server, stop_grpc_server

    import jwt as pyjwt

    server = await start_grpc_health_server()
    bound_port = getattr(server, "_fastmvc_bound_port")

    try:
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{bound_port}")
        stub = user_pb2_grpc.UserServiceStub(channel)

        payload = {"sub": "user-1", "exp": int(time.time()) + 60}
        token = pyjwt.encode(payload, "a_very_long_and_complex_secret_key!", algorithm="HS256")

        resp = await stub.FetchUser(
            user_pb2.FetchUserRequest(name="alice", description="dev"),
            metadata=[("authorization", f"Bearer {token}")],
            timeout=2.0,
        )
        assert resp.id == "1"
        assert resp.message == "Success"
        assert resp.status == "active"
    finally:
        await stop_grpc_server(server)

