import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

MEM0_TELEMETRY = os.environ.get("MEM0_TELEMETRY", "True")

if isinstance(MEM0_TELEMETRY, str):
    MEM0_TELEMETRY = MEM0_TELEMETRY.lower() in ("true", "1", "yes")


def use_telemetry():
    if os.getenv("MEM0_TELEMETRY", "true").lower() == "true":
        return True
    return False


@pytest.fixture(autouse=True)
def reset_env():
    with patch.dict(os.environ, {}, clear=True):
        yield


def test_telemetry_enabled():
    with patch.dict(os.environ, {"MEM0_TELEMETRY": "true"}):
        assert use_telemetry() is True


def test_telemetry_disabled():
    with patch.dict(os.environ, {"MEM0_TELEMETRY": "false"}):
        assert use_telemetry() is False


def test_telemetry_default_enabled():
    assert use_telemetry() is True


def test_capture_event_reuses_memory_telemetry_client():
    from mem0.memory import telemetry

    memory_instance = SimpleNamespace(
        collection_name="test",
        embedding_model=SimpleNamespace(config=SimpleNamespace(embedding_dims=3)),
        graph=object(),
        vector_store=object(),
        llm=object(),
        config=SimpleNamespace(graph_store=SimpleNamespace(config={})),
        api_version="v1.1",
    )
    shared_client = MagicMock()

    with (
        patch.object(telemetry, "memory_telemetry", shared_client),
        patch.object(telemetry, "AnonymousTelemetry") as telemetry_constructor,
    ):
        telemetry.capture_event("mem0.search", memory_instance)
        telemetry.capture_event("mem0.search", memory_instance)

    telemetry_constructor.assert_not_called()
    assert shared_client.capture_event.call_count == 2
