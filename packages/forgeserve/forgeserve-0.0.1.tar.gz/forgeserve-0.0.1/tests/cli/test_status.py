from typer.testing import CliRunner
from forgeserve.cli.main import app
from forgeserve.runners.base import DeploymentStatus
from unittest.mock import patch, MagicMock, call

runner = CliRunner()

@pytest.fixture
def mock_managers():
    """Fixture to mock DeploymentManager and StatusManager."""

    with patch('forgeserve.cli.status.StatusManager') as mock_stat_mgr_cls_status:

 
        mock_deployment_manager = MagicMock()
        mock_status_manager = MagicMock()

        mock_stat_mgr_cls_status.return_value = mock_status_manager


        yield mock_deployment_manager, mock_status_manager


def test_status_success(mock_managers):
    """Test `status` command successfully retrieving status."""
    _, mock_status_manager = mock_managers
    deployment_name = "my-app"
    namespace = "dev"
    # Prepare mock status data matching DeploymentStatus structure
    mock_status_data = DeploymentStatus(
        name=deployment_name,
        namespace=namespace,
        desired_replicas=2,
        ready_replicas=2,
        pods=[
            {"name": "my-app-pod-1", "status": "Running", "ready": True, "node": "node-a", "startTime": "2023-01-01T10:00:00Z"},
            {"name": "my-app-pod-2", "status": "Running", "ready": True, "node": "node-b", "startTime": "2023-01-01T10:01:00Z"},
        ],
        service_endpoint="10.0.0.5:8000"
    )
    mock_status_manager.get_status.return_value = mock_status_data

    result = runner.invoke(app, ["status", deployment_name, "-n", namespace])

    assert result.exit_code == 0
    assert f"Checking status for deployment '{deployment_name}'" in result.stdout
    assert f"Status for Deployment: {deployment_name}" in result.stdout
    assert "Desired Replicas:" in result.stdout
    assert "Ready Replicas:" in result.stdout
    assert " 2" in result.stdout # Check if replicas count is displayed
    assert "Service Endpoint:" in result.stdout
    assert "10.0.0.5:8000" in result.stdout
    assert "Pods" in result.stdout # Table title
    assert "my-app-pod-1" in result.stdout
    assert "my-app-pod-2" in result.stdout
    assert "node-a" in result.stdout
    mock_status_manager.get_status.assert_called_once_with(deployment_name, namespace)

def test_status_not_found(mock_managers):
    """Test `status` command when deployment is not found."""
    _, mock_status_manager = mock_managers
    deployment_name = "not-found-app"
    namespace = "default"
    mock_status_manager.get_status.return_value = None # Simulate not found

    result = runner.invoke(app, ["status", deployment_name, "-n", namespace])

    assert result.exit_code == 1 # Exit code 1 for not found
    assert f"Deployment '{deployment_name}' not found" in result.stdout
    mock_status_manager.get_status.assert_called_once_with(deployment_name, namespace)

def test_status_manager_error(mock_managers):
    """Test `status` command when manager raises an error."""
    _, mock_status_manager = mock_managers
    deployment_name = "status-error"
    namespace = "default"
    error_message = "Simulated error fetching status"
    mock_status_manager.get_status.side_effect = Exception(error_message)

    result = runner.invoke(app, ["status", deployment_name, "-n", namespace])

    assert result.exit_code != 0
    assert f"Error fetching status for '{deployment_name}'" in result.stdout
    assert error_message in result.stdout
    mock_status_manager.get_status.assert_called_once_with(deployment_name, namespace)