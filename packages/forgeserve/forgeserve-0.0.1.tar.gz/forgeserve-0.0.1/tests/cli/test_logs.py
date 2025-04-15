from typer.testing import CliRunner
from forgeserve.cli.main import app
from forgeserve.runners.base import DeploymentStatus
from unittest.mock import patch, MagicMock, call

runner = CliRunner()

@pytest.fixture
def mock_managers():
    """Fixture to mock DeploymentManager and StatusManager."""

    with patch('forgeserve.cli.logs.StatusManager') as mock_stat_mgr_cls_logs:


        mock_deployment_manager = MagicMock()
        mock_status_manager = MagicMock() 

        mock_stat_mgr_cls_logs.return_value = mock_status_manager


        yield mock_deployment_manager, mock_status_manager

def test_logs_success_no_follow(mock_managers):
    """Test `logs` command fetching historical logs."""
    _, mock_status_manager = mock_managers
    deployment_name = "log-app"
    namespace = "logging"
    log_lines = ["Log line 1", "ERROR: Something went wrong", "Log line 3"]

    # Mock the generator returned by stream_logs
    mock_status_manager.stream_logs.return_value = (line for line in log_lines)

    result = runner.invoke(app, ["logs", deployment_name, "-n", namespace])

    assert result.exit_code == 0
    assert f"Fetching logs for deployment '{deployment_name}'" in result.stdout
    # Check if log lines are present (rich might add formatting)
    assert "Log line 1" in result.stdout
    assert "ERROR: Something went wrong" in result.stdout
    assert "Log line 3" in result.stdout
    # Check the call arguments to the manager
    mock_status_manager.stream_logs.assert_called_once_with(deployment_name, namespace, False, None) # follow=False, tail=None

def test_logs_success_follow_and_tail(mock_managers):
    """Test `logs` command with --follow and --tail options."""
    _, mock_status_manager = mock_managers
    deployment_name = "stream-app"
    namespace = "realtime"
    log_lines = ["Older line", "Recent line 1", "Recent line 2"]
    tail_count = 2

    mock_status_manager.stream_logs.return_value = (line for line in log_lines) # Simulate finite stream for test

    result = runner.invoke(app, ["logs", deployment_name, "-n", namespace, "--follow", "--tail", str(tail_count)])

    assert result.exit_code == 0
    assert f"Streaming logs for deployment '{deployment_name}'" in result.stdout
    assert f"Showing last {tail_count} lines" in result.stdout
    assert "(Press Ctrl+C to stop streaming)" in result.stdout
    # Check output
    assert "Older line" in result.stdout # In this simple mock, tail doesn't filter history, K8s API does
    assert "Recent line 1" in result.stdout
    assert "Recent line 2" in result.stdout
    # Check call arguments
    mock_status_manager.stream_logs.assert_called_once_with(deployment_name, namespace, True, tail_count) # follow=True, tail=2


def test_logs_no_pods_found(mock_managers):
    """Test `logs` command when the manager finds no pods (returns empty generator)."""
    _, mock_status_manager = mock_managers
    deployment_name = "no-pod-app"
    namespace = "default"

    # Simulate no logs found by returning an empty generator
    mock_status_manager.stream_logs.return_value = (line for line in [])

    result = runner.invoke(app, ["logs", deployment_name, "-n", namespace])

    assert result.exit_code == 0 # Exits cleanly, just prints nothing
    # Check that stream_logs was still called
    mock_status_manager.stream_logs.assert_called_once_with(deployment_name, namespace, False, None)
    # Check if a "no pods found" message is printed (this depends on runner/manager implementation)
    # assert "No pods found" or "No logs found" in result.stdout - Add if your code prints this

def test_logs_manager_error(mock_managers):
    """Test `logs` command when manager raises an error during streaming."""
    _, mock_status_manager = mock_managers
    deployment_name = "log-error-app"
    namespace = "default"
    error_message = "Simulated error fetching logs"

    # Make the generator raise an exception when iterated
    def error_generator():
        yield "First line"
        raise Exception(error_message)
        # yield "This won't be reached" # Optional

    mock_status_manager.stream_logs.return_value = error_generator()

    result = runner.invoke(app, ["logs", deployment_name, "-n", namespace])

    assert result.exit_code != 0
    assert "First line" in result.stdout # Check that lines before error are printed
    assert f"Error fetching logs for '{deployment_name}'" in result.stdout
    assert error_message in result.stdout
    mock_status_manager.stream_logs.assert_called_once_with(deployment_name, namespace, False, None)