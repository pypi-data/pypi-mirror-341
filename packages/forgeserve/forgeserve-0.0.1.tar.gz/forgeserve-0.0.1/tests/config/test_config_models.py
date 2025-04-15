# tests/config/test_config_models.py

import pytest
from pydantic import ValidationError

# Assuming your models are importable like this
from forgeserve.config.models import (
    DeploymentConfig,
    BackendConfig,
    ResourceRequests,
    ResourceSpec,
    ModelStorageConfig,
    OllamaConfig,
    Toleration
)

# --- Fixtures for Sample Config Data ---

@pytest.fixture
def minimal_vllm_dict():
    return {
        "name": "test-vllm",
        "model": {"source": "huggingface", "identifier": "gpt2"},
        "resources": {
            "requests": {"cpu": "1", "memory": "4Gi", "nvidia.com/gpu": 1}
        },
        "backend": {"adapter": "vllm"}, # No explicit vllm_config
    }

@pytest.fixture
def minimal_ollama_dict():
    return {
        "name": "test-ollama",
        "model": {"source": "huggingface", "identifier": "llama3"},
        "resources": {
            "requests": {"cpu": "1", "memory": "8Gi"} # No GPU initially
        },
        "backend": {"adapter": "ollama"}, # No explicit ollama_config
    }

@pytest.fixture
def full_ollama_dict():
    return {
        "name": "ollama-full",
        "namespace": "ai-apps",
        "replicas": 2,
        "model": {"source": "huggingface", "identifier": "mistral"},
        "resources": {
            "requests": {"cpu": "2", "memory": "16Gi", "nvidia.com/gpu": 1},
            "limits": {"memory": "32Gi", "nvidia.com/gpu": 1},
        },
        "backend": {
            "adapter": "ollama",
            "port": 11435,
            "config": {
                "ollama": { # Using alias 'ollama'
                    "num_gpu": 1,
                    "keep_alive": "5m"
                }
            }
        },
        "model_storage": {
            "pvc_name": "my-ollama-pvc",
            "mount_path": "/data"
        },
        "tolerations": [
            {"key": "team", "operator": "Equal", "value": "ai", "effect": "NoSchedule"}
        ]
    }

# --- Test Cases ---

def test_load_minimal_vllm(minimal_vllm_dict):
    """Test loading minimal vLLM config, validator should add empty vllm_config."""
    config = DeploymentConfig(**minimal_vllm_dict)
    assert config.name == "test-vllm"
    assert config.backend.adapter == "vllm"
    assert config.backend.port == 8000 # Should default correctly for vllm
    assert config.backend.config.vllm_config is not None
    assert config.backend.config.ollama_config is None
    # Check direct GPU parsing
    assert config.resources.requests.nvidia_gpu == 1
    assert config.resources.limits is None # No limits specified
    assert not config.tolerations # No custom tolerations
    assert config.model_storage is None

def test_load_minimal_ollama(minimal_ollama_dict):
    """Test loading minimal Ollama config, validator should add empty ollama_config."""
    config = DeploymentConfig(**minimal_ollama_dict)
    assert config.name == "test-ollama"
    assert config.backend.adapter == "ollama"
    assert config.backend.port == 11434 # Should default correctly for ollama
    assert config.backend.config.ollama_config is not None
    assert config.backend.config.vllm_config is None
    # Check GPU parsing (should be None)
    assert config.resources.requests.nvidia_gpu is None
    assert not config.tolerations
    assert config.model_storage is None

def test_load_full_ollama(full_ollama_dict):
    """Test loading a more complex Ollama config."""
    config = DeploymentConfig(**full_ollama_dict)
    assert config.name == "ollama-full"
    assert config.namespace == "ai-apps"
    assert config.replicas == 2
    assert config.resources.requests.nvidia_gpu == 1
    assert config.resources.limits.nvidia_gpu == 1
    assert config.resources.requests.memory == "16Gi"
    assert config.backend.adapter == "ollama"
    assert config.backend.port == 11435 # Port override
    assert config.backend.config.ollama_config.num_gpu == 1
    assert config.backend.config.ollama_config.keep_alive == "5m"
    assert config.model_storage.pvc_name == "my-ollama-pvc"
    assert config.model_storage.mount_path == "/data"
    assert len(config.tolerations) == 1
    assert config.tolerations[0].key == "team"
    assert config.tolerations[0].value == "ai"

def test_gpu_resource_validation():
    """Test validation for GPU count."""
    with pytest.raises(ValidationError, match="nvidia.com/gpu"):
        ResourceRequests(cpu="1", memory="1Gi", **{"nvidia.com/gpu": 0}) # Using dict expansion for alias

    with pytest.raises(ValidationError, match="'nvidia.com/gpu' limits must be greater than or equal to requests"):
        ResourceSpec(
            requests=ResourceRequests(**{"nvidia.com/gpu": 2}),
            limits=ResourceRequests(**{"nvidia.com/gpu": 1})
        )

    # Should pass
    spec = ResourceSpec(
            requests=ResourceRequests(**{"nvidia.com/gpu": 1}),
            limits=ResourceRequests(**{"nvidia.com/gpu": 1})
        )
    assert spec.requests.nvidia_gpu == 1
    assert spec.limits.nvidia_gpu == 1

def test_toleration_validation():
    """Test custom toleration validation."""
    # Value required for Equal operator
    with pytest.raises(ValidationError, match="Toleration value is required"):
        Toleration(key="test", operator="Equal", effect="NoSchedule")

    # tolerationSeconds only valid for NoExecute
    with pytest.raises(ValidationError, match="tolerationSeconds can only be specified"):
        Toleration(key="test", operator="Exists", effect="NoSchedule", tolerationSeconds=10)

    # Should pass
    Toleration(key="test", operator="Exists", effect="NoExecute", tolerationSeconds=10)
    Toleration(key="test", operator="Exists", effect="NoSchedule")
    Toleration(key="test", operator="Equal", value="abc", effect="NoSchedule")
    Toleration(operator="Exists") # Tolerate everything