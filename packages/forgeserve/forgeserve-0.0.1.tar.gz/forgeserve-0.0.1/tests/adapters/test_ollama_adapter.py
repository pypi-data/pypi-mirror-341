# tests/adapters/test_ollama_adapter.py

import pytest

from forgeserve.config.models import (
    DeploymentConfig, ModelSource, ResourceSpec, ResourceRequests,
    BackendConfig, BackendAdapterConfig, OllamaConfig, ModelStorageConfig
)
from forgeserve.adapters.ollama import OllamaAdapter

# --- Helper to create a config object ---
def create_test_config(
    gpu_count: int = 0,
    ollama_cfg_dict: dict = None,
    model_storage_cfg: dict = None,
    backend_port: int = 11434
) -> DeploymentConfig:
    """Creates a DeploymentConfig for testing the Ollama adapter."""
    resources_dict = {"requests": {"cpu": "1", "memory": "4Gi"}}
    if gpu_count > 0:
        resources_dict["requests"]["nvidia.com/gpu"] = gpu_count
        # Add default limits if GPUs requested
        resources_dict["limits"] = {"nvidia.com/gpu": gpu_count}

    adapter_config = BackendAdapterConfig()
    if ollama_cfg_dict is not None:
        adapter_config.ollama_config = OllamaConfig(**ollama_cfg_dict)

    backend_conf = BackendConfig(
        adapter="ollama",
        port=backend_port,
        config=adapter_config
    )
    # Run validator manually if needed (should happen on creation)
    # backend_conf = BackendConfig.model_validate(backend_conf.model_dump())

    storage = ModelStorageConfig(**model_storage_cfg) if model_storage_cfg else None

    return DeploymentConfig(
        name="test-ollama-deploy",
        model=ModelSource(source="huggingface", identifier="llama3"),
        resources=ResourceSpec(**resources_dict),
        backend=backend_conf,
        model_storage=storage
    )

# --- Test Cases ---

def test_ollama_adapter_name():
    config = create_test_config()
    adapter = OllamaAdapter(config)
    assert adapter.adapter_name == "ollama"

def test_ollama_container_spec_basic():
    """Test basic container spec generation (CPU only, no PVC)."""
    config = create_test_config(gpu_count=0)
    adapter = OllamaAdapter(config)
    spec = adapter.get_container_spec()

    assert spec["image"] == "ollama/ollama:latest"
    assert spec["ports"] == [{"containerPort": 11434, "name": "http"}]
    assert spec["volumeMounts"] is None # No PVC requested
    assert "nvidia.com/gpu" not in spec["resources"].get("limits", {})
    assert spec["resources"]["requests"]["cpu"] == "1"

    env_dict = {e["name"]: e["value"] for e in spec["env"]}
    assert env_dict["OLLAMA_HOST"] == "0.0.0.0:11434"
    assert "OLLAMA_NUM_GPU" not in env_dict # No GPU requested, default behavior
    assert "OLLAMA_MODELS" not in env_dict
    assert "OLLAMA_KEEP_ALIVE" not in env_dict

def test_ollama_container_spec_with_gpu():
    """Test spec generation with GPU request."""
    config = create_test_config(gpu_count=1, ollama_cfg_dict={"num_gpu": 1})
    adapter = OllamaAdapter(config)
    spec = adapter.get_container_spec()

    assert spec["resources"]["limits"]["nvidia.com/gpu"] == "1"

    env_dict = {e["name"]: e["value"] for e in spec["env"]}
    assert env_dict["OLLAMA_NUM_GPU"] == "1"

def test_ollama_container_spec_with_config_overrides():
    """Test spec generation with custom Ollama config."""
    config = create_test_config(
        ollama_cfg_dict={"keep_alive": "1h", "models_dir": "/models"}
    )
    adapter = OllamaAdapter(config)
    spec = adapter.get_container_spec()

    env_dict = {e["name"]: e["value"] for e in spec["env"]}
    assert env_dict["OLLAMA_MODELS"] == "/models"
    assert env_dict["OLLAMA_KEEP_ALIVE"] == "1h"

def test_ollama_container_spec_with_pvc():
    """Test spec generation with PVC for model storage."""
    config = create_test_config(
        model_storage_cfg={"pvc_name": "my-models-pvc", "mount_path": "/data/ollama"}
    )
    adapter = OllamaAdapter(config)
    spec = adapter.get_container_spec()

    assert len(spec["volumeMounts"]) == 1
    assert spec["volumeMounts"][0]["name"] == "ollama-models-storage"
    assert spec["volumeMounts"][0]["mountPath"] == "/data/ollama"

def test_ollama_get_volumes_no_pvc():
    config = create_test_config()
    adapter = OllamaAdapter(config)
    volumes = adapter.get_volumes()
    assert volumes is None

def test_ollama_get_volumes_with_pvc():
    config = create_test_config(
        model_storage_cfg={"pvc_name": "ollama-data"}
    )
    adapter = OllamaAdapter(config)
    volumes = adapter.get_volumes()
    assert len(volumes) == 1
    assert volumes[0]["name"] == "ollama-models-storage"
    assert volumes[0]["persistentVolumeClaim"]["claimName"] == "ollama-data"

def test_ollama_probes():
    """Test probe generation."""
    config = create_test_config(backend_port=12345)
    adapter = OllamaAdapter(config)

    readiness = adapter.get_readiness_probe()
    liveness = adapter.get_liveness_probe()

    assert readiness["httpGet"]["path"] == "/"
    assert readiness["httpGet"]["port"] == 12345
    assert liveness["httpGet"]["path"] == "/"
    assert liveness["httpGet"]["port"] == 12345