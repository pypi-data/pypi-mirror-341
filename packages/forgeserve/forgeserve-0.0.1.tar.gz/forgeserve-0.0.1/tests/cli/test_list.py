from typer.testing import CliRunner
from forgeserve.cli.main import app
from forgeserve.runners.base import DeploymentStatus
from unittest.mock import patch, MagicMock, call

runner = CliRunner()

@pytest.fixture
def mock_managers():
    """Fixture to mock DeploymentManager and StatusManager."""
    # Patch the *location where they are imported* in the CLI command modules
    with patch('forgeserve.cli.list_deployments.StatusManager') as mock_stat_mgr_cls_list:

        # Create mock instances
        mock_deployment_manager = MagicMock()
        mock_status_manager = MagicMock() # Use one instance for status, list, logs

        mock_stat_mgr_cls_list.return_value = mock_status_manager

        # Yield the instances to the tests
        yield mock_deployment_manager, mock_status_manager

def test_list_success_with_deployments(mock_managers):
    """Test `list` command when deployments are found."""
    _, mock_status_manager = mock_managers
    namespace = "production"
    mock_deployments = [
        {"name": "app-alpha", "namespace": namespace, "replicas": 1, "ready": 1},
        {"name": "app-beta", "namespace": namespace, "replicas": 3, "ready": 2}, # Example of not fully ready
    ]
    mock_status_manager.list_deployments.return_value = mock_deployments

    result = runner.invoke(app, ["list", "-n", namespace])

    assert result.exit_code == 0
    assert f"Listing ForgeServe deployments in namespace '{namespace}'" in result.stdout
    assert "Name" in result.stdout # Check table header
    assert "Namespace" in result.stdout
    assert "Desired" in result.stdout
    assert "Ready" in result.stdout
    assert "app-alpha" in result.stdout
    assert "app-beta" in result.stdout
    assert " 1" in result.stdout # Ready/Desired counts
    assert " 3" in result.stdout
    assert " 2" in result.stdout
    mock_status_manager.list_deployments.assert_called_once_with(namespace)

def test_list_success_no_deployments(mock_managers):
    """Test `list` command when no deployments are found."""
    _, mock_status_manager = mock_managers
    namespace = "empty-ns"
    mock_status_manager.list_deployments.return_value = [] # Simulate empty list

    result = runner.invoke(app, ["list", "-n", namespace])

    assert result.exit_code == 0 # Should exit cleanly even if empty
    assert f"No ForgeServe deployments found in namespace '{namespace}'" in result.stdout
    mock_status_manager.list_deployments.assert_called_once_with(namespace)

def test_list_manager_error(mock_managers):
    """Test `list` command when manager raises an error."""
    _, mock_status_manager = mock_managers
    namespace = "error-ns"
    error_message = "Simulated error listing deployments"
    mock_status_manager.list_deployments.side_effect = Exception(error_message)

    result = runner.invoke(app, ["list", "-n", namespace])

    assert result.exit_code != 0
    assert "Error listing deployments" in result.stdout
    assert error_message in result.stdout
    mock_status_manager.list_deployments.assert_called_once_with(namespace)
