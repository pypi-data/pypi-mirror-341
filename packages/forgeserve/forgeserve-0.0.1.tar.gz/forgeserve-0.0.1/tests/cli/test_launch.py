# tests/cli/test_launch.py

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

# Import the main Typer app object
from forgeserve.cli.main import app
from forgeserve.config.models import DeploymentConfig

runner = CliRunner()

# --- Test Cases ---

@pytest.fixture
def mock_deps():
    """Fixture to mock dependencies (Runner, Manager)."""
    with patch('forgeserve.cli.launch.KubernetesRunner') as mock_runner_cls, \
         patch('forgeserve.cli.launch.DeploymentManager') as mock_manager_cls:
        # Configure the mock manager instance that will be created
        mock_manager_instance = MagicMock()
        mock_manager_cls.return_value = mock_manager_instance
        yield mock_runner_cls, mock_manager_instance # Return manager *instance*

# --- Config File Tests ---

def test_launch_with_config_success(tmp_path, mock_deps):
    """Test launching with a valid config file."""
    mock_runner_cls, mock_manager = mock_deps
    config_content = """
name: test-app-from-file
model: {source: huggingface, identifier: gpt2}
resources:
  requests: {cpu: 1, memory: 1Gi}
backend: {adapter: vllm}
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    result = runner.invoke(app, ["launch", "--config", str(config_file)])

    assert result.exit_code == 0
    assert "Loading configuration from file" in result.stdout
    assert "Initializing deployment for 'test-app-from-file'" in result.stdout
    assert "Successfully initiated launch" in result.stdout
    mock_manager.launch.assert_called_once()
    # Check the config passed to the manager
    call_args, _ = mock_manager.launch.call_args
    launched_config = call_args[0]
    assert isinstance(launched_config, DeploymentConfig)
    assert launched_config.name == "test-app-from-file"
    assert launched_config.backend.adapter == "vllm"

def test_launch_with_config_and_namespace_override(tmp_path, mock_deps):
    """Test --namespace override with config file."""
    mock_runner_cls, mock_manager = mock_deps
    config_content = """
name: test-app-ns
namespace: from-file-ns # Namespace defined in file
model: {source: huggingface, identifier: gpt2}
resources: {requests: {cpu: 1}}
backend: {adapter: vllm}
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    result = runner.invoke(app, ["launch", "--config", str(config_file), "-n", "override-ns"])

    assert result.exit_code == 0
    mock_manager.launch.assert_called_once()
    launched_config = mock_manager.launch.call_args[0][0]
    assert launched_config.namespace == "override-ns" # Check override worked

def test_launch_with_config_and_quick_launch_opts(tmp_path, mock_deps):
    """Test warning/error when mixing config file and quick launch options."""
    mock_runner_cls, mock_manager = mock_deps
    config_content = "name: test\nmodel: {source: hf, id: g}\nresources: {req: {c: 1}}\nbackend: {adapter: vllm}" # Simplified for brevity
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    # Using --gpus with --config
    result = runner.invoke(app, ["launch", "--config", str(config_file), "--gpus", "1"])

    # Depending on whether you chose warning or error:
    # Option 1: Warning (exit code 0, prints warning)
    # assert result.exit_code == 0
    # assert "Warning: Quick launch options" in result.stdout
    # mock_manager.launch.assert_called_once() # Launch should still happen

    # Option 2: Error (exit code non-zero, no launch call)
    assert result.exit_code != 0 # Or check specific exit code if Typer uses one
    assert "Error: Cannot use quick launch options" in result.stdout # Adjust error message if needed
    mock_manager.launch.assert_not_called()

# --- Quick Launch Tests ---

def test_launch_with_model_id_success(mock_deps):
    """Test basic quick launch with model ID."""
    mock_runner_cls, mock_manager = mock_deps
    model_id = "openai-community/gpt2"
    result = runner.invoke(app, ["launch", model_id])

    assert result.exit_code == 0
    assert f"Preparing quick launch for model ID: {model_id}" in result.stdout
    assert "Generating default configuration" in result.stdout
    assert "Initializing deployment" in result.stdout
    assert "Successfully initiated launch" in result.stdout
    mock_manager.launch.assert_called_once()
    # Check config passed
    launched_config = mock_manager.launch.call_args[0][0]
    assert isinstance(launched_config, DeploymentConfig)
    assert launched_config.model.identifier == model_id
    assert launched_config.backend.adapter == "vllm" # Default backend
    assert launched_config.resources.requests.nvidia_gpu == 1 # Default GPU count
    assert launched_config.name == "openai-community-gpt2-serving" # Auto-generated name

def test_launch_quick_ollama_backend(mock_deps):
    """Test quick launch specifying Ollama backend and GPUs."""
    mock_runner_cls, mock_manager = mock_deps
    model_id = "llama3"
    result = runner.invoke(app, ["launch", model_id, "--backend", "ollama", "--gpus", "1", "-n", "ollama-ns", "--name", "my-llama"])

    assert result.exit_code == 0
    assert f"Preparing quick launch for model ID: {model_id}" in result.stdout
    assert "Backend Adapter: ollama" in result.stdout
    assert "GPU Count:       1" in result.stdout
    assert "Ollama Config:   num_gpu=1" in result.stdout # Check generated config log
    mock_manager.launch.assert_called_once()
    # Check config passed
    launched_config = mock_manager.launch.call_args[0][0]
    assert launched_config.model.identifier == model_id
    assert launched_config.backend.adapter == "ollama"
    assert launched_config.resources.requests.nvidia_gpu == 1
    assert launched_config.namespace == "ollama-ns"
    assert launched_config.name == "my-llama" # Name override
    assert launched_config.backend.config.ollama_config is not None
    assert launched_config.backend.config.ollama_config.num_gpu == 1


# --- Error Condition Tests ---

def test_launch_mutually_exclusive_error(tmp_path, mock_deps):
    """Test error when both --config and model ID are provided."""
    mock_runner_cls, mock_manager = mock_deps
    config_file = tmp_path / "config.yaml"
    config_file.touch() # File just needs to exist
    result = runner.invoke(app, ["launch", "--config", str(config_file), "some-model-id"])

    assert result.exit_code != 0
    assert "Error: Cannot use both --config option and MODEL_ID argument" in result.stdout
    mock_manager.launch.assert_not_called()

def test_launch_missing_input_error(mock_deps):
    """Test error when neither --config nor model ID is provided."""
    mock_runner_cls, mock_manager = mock_deps
    result = runner.invoke(app, ["launch"])

    assert result.exit_code != 0
    assert "Error: Must provide either --config option or a MODEL_ID argument" in result.stdout
    mock_manager.launch.assert_not_called()

def test_launch_config_not_found_error(mock_deps):
    """Test error when --config file doesn't exist."""
    mock_runner_cls, mock_manager = mock_deps
    result = runner.invoke(app, ["launch", "--config", "nonexistent_file.yaml"])

    assert result.exit_code != 0
    # Typer usually handles "does not exist" error message itself
    assert "Invalid value for '--config' / '-c'" in result.stdout
    assert "does not exist" in result.stdout
    mock_manager.launch.assert_not_called()