from typer.testing import CliRunner
from forgeserve.cli.main import app
from forgeserve.runners.base import DeploymentStatus
from unittest.mock import patch, MagicMock, call

runner = CliRunner()

@pytest.fixture
def mock_managers():
    """Fixture to mock DeploymentManager and StatusManager."""

    with patch('forgeserve.cli.delete.DeploymentManager') as mock_dep_mgr_cls:


        mock_deployment_manager = MagicMock()
        mock_status_manager = MagicMock() #
        mock_dep_mgr_cls.return_value = mock_deployment_manager

        yield mock_deployment_manager, mock_status_manager

def test_delete_success_confirm(mock_managers):
    """Test `delete` command with confirmation 'y'."""
    mock_deployment_manager, _ = mock_managers
    deployment_name = "test-to-delete"
    namespace = "staging"

    result = runner.invoke(app, ["delete", deployment_name, "-n", namespace], input="y\n")

    assert result.exit_code == 0
    assert f"Preparing to delete deployment '{deployment_name}'" in result.stdout
    assert "Are you sure you want to delete" in result.stdout
    assert "Successfully initiated teardown" in result.stdout
    mock_deployment_manager.delete.assert_called_once_with(deployment_name, namespace)

def test_delete_success_force(mock_managers):
    """Test `delete` command with --force option."""
    mock_deployment_manager, _ = mock_managers
    deployment_name = "force-delete-me"
    namespace = "default"

    result = runner.invoke(app, ["delete", deployment_name, "-n", namespace, "--force"]) # Or -y

    assert result.exit_code == 0
    assert f"Preparing to delete deployment '{deployment_name}'" in result.stdout
    assert "Are you sure" not in result.stdout # No confirmation prompt
    assert "Successfully initiated teardown" in result.stdout
    mock_deployment_manager.delete.assert_called_once_with(deployment_name, namespace)

def test_delete_abort_confirm(mock_managers):
    """Test `delete` command aborted with confirmation 'n'."""
    mock_deployment_manager, _ = mock_managers
    deployment_name = "dont-delete"
    namespace = "prod"

    result = runner.invoke(app, ["delete", deployment_name, "-n", namespace], input="n\n")

    assert result.exit_code == 1 # Exit code 1 for aborted action typically
    assert "Are you sure" in result.stdout
    assert "Aborted deletion" in result.stdout
    mock_deployment_manager.delete.assert_not_called() # Ensure manager method wasn't called

def test_delete_manager_error(mock_managers):
    """Test `delete` command when manager raises an error."""
    mock_deployment_manager, _ = mock_managers
    deployment_name = "error-prone"
    namespace = "default"
    error_message = "Simulated K8s API error during delete"
    mock_deployment_manager.delete.side_effect = Exception(error_message)

    result = runner.invoke(app, ["delete", deployment_name, "-n", namespace, "--force"])

    assert result.exit_code != 0 # Should exit with non-zero code on error
    assert f"Error during teardown for '{deployment_name}'" in result.stdout
    assert error_message in result.stdout
    mock_deployment_manager.down.assert_called_once_with(deployment_name, namespace)
