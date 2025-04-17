from typing import TYPE_CHECKING, Union

from wtwco_igloo.api_client import AuthenticatedClient
from wtwco_igloo.api_client.api.workspaces import create_workspace, list_workspaces
from wtwco_igloo.api_client.models import CreateWorkspace, WorkspaceArrayResponse, WorkspaceResponse
from wtwco_igloo.api_client.models import Workspace as ClientWorkspace
from wtwco_igloo.extensions.utils.authentication.authentication_with_refresh import _AuthenticationManagerWithRefresh
from wtwco_igloo.extensions.utils.authentication.authentication_without_refresh import (
    _AuthenticationManagerWithoutRefresh,
)
from wtwco_igloo.extensions.utils.errors.workspace_errors import WorkspaceNotFoundError
from wtwco_igloo.extensions.utils.errors.wtwco_igloo_errors import _log_and_get_exception
from wtwco_igloo.extensions.utils.helpers import _standardise_url
from wtwco_igloo.extensions.utils.validators.response_validator import _ResponseValidator

if TYPE_CHECKING:
    from wtwco_igloo import Workspace


class Connection(object):
    """Handles connecting to the WTW Igloo Cloud and initial functionality.

    The connection class is constructed via the class methods `from_device_code`, `from_interactive_token`,
    `from_certificate`, and `from_secret`. These class methods cover the different ways to authenticate to Azure and
    all return a connection instance.

    Attributes:
        web_app_url (str): Igloo Cloud Web App URL.
        post_data_row_batch_size (int): Defines the number of rows of data to send at a time when updating a data table, defaults to 10,000
    """

    def __init__(
        self,
        authentication_manager: Union[_AuthenticationManagerWithoutRefresh, _AuthenticationManagerWithRefresh],
        run_processing_minutes: int,
    ) -> None:
        self.web_app_url: str = _standardise_url(authentication_manager._api_url, "/manager/")
        self.post_data_row_batch_size: int = 10000
        self._authentication_manager = authentication_manager
        self._run_processing_minutes = run_processing_minutes
        self._validate_response = _ResponseValidator._validate_response
        self._import_classes()

    def __str__(self) -> str:
        return self.web_app_url

    @classmethod
    def from_certificate(
        cls,
        api_url: str,
        client_id: str,
        thumbprint: str,
        certificate_path: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
    ) -> "Connection":
        """Connect to Igloo Cloud using a certificate.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            thumbprint: Certificate thumbprint.
            certificate_path: Path to .pem certificate file.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_certificate(thumbprint, certificate_path)

        return cls(authentication_manager, run_processing_minutes)

    @classmethod
    def from_device_code(
        cls,
        api_url: str,
        client_id: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
        **kwargs: bool,
    ) -> "Connection":
        """Connect to Igloo Cloud using device code flow.

        After connecting your device will be remembered for future connections.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.
            **kwargs: Additional keyword arguments used for testing only.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_device_code(**kwargs)

        return cls(authentication_manager, run_processing_minutes)

    @classmethod
    def from_interactive_token(
        cls,
        api_url: str,
        client_id: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
        **kwargs: bool,
    ) -> "Connection":
        """Connect to Igloo Cloud using interactive token.

        After connecting your device will be remembered for future connections.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.
            **kwargs: Additional keyword arguments used for testing only.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_interactive_token(**kwargs)

        return cls(authentication_manager, run_processing_minutes)

    @classmethod
    def from_secret(
        cls,
        api_url: str,
        client_id: str,
        secret: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
    ) -> "Connection":
        """Connect to Igloo Cloud using a secret.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            secret: Secret for authenticating with tenant.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_secret(secret)

        return cls(authentication_manager, run_processing_minutes)

    def get_workspaces(self) -> list["Workspace"]:
        """Retrieves the list of workspaces available to the API.

        Returns:
            List of available workspaces.

        Raises:
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        response = list_workspaces.sync_detailed(client=self._get_authenticated_client())
        raw_workspaces: list[ClientWorkspace] = self._validate_response(
            response, WorkspaceArrayResponse, ClientWorkspace
        )
        return [Workspace(self, ws.to_dict()) for ws in raw_workspaces]

    def get_workspace(self, workspace_name: str) -> "Workspace":
        """Retrieves the project with the given name.

        Args:
            project_name: Name of project to return.

        Returns:
            Project with the given name.

        Raises:
            WorkspaceNotFoundError: Workspace with the given name was not found.
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        workspaces = self.get_workspaces()
        for workspace in workspaces:
            if workspace.name == workspace_name:
                return workspace
        raise _log_and_get_exception(WorkspaceNotFoundError, f"Workspace {workspace_name} not found.")

    def create_workspace(
        self,
        name: str,
        description: str = "",
    ) -> "Workspace":
        """Creates a new Workspace.

        Args:
            name: The name given to the new workspace. Maximum of 100 characters and must be unique across the environment.
            description: Description of the workspace. Defaults to "".

        Returns:
            The newly created workspace.

        Raises:
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        workspace_to_create = CreateWorkspace(
            name=name,
            description=description,
        )

        response = create_workspace.sync_detailed(
            client=self._get_authenticated_client(),
            body=workspace_to_create,
        )
        raw_workspace: ClientWorkspace = self._validate_response(response, WorkspaceResponse, ClientWorkspace)
        return Workspace(self, raw_workspace.to_dict())

    def _get_authenticated_client(self) -> AuthenticatedClient:
        return self._authentication_manager._get_authenticated_client()

    @staticmethod
    def _import_classes() -> None:
        """Import classes to avoid circular imports."""
        global Model, Project, Workspace
        from wtwco_igloo import Model, Project, Workspace
