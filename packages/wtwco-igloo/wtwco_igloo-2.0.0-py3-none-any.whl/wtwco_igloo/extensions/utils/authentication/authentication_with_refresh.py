from msal import ConfidentialClientApplication, PublicClientApplication
from wtwco_igloo_cloud_api_client import AuthenticatedClient

from wtwco_igloo.extensions.utils.authentication.authentication_base import _AuthenticationManagerBase
from wtwco_igloo.extensions.utils.errors.connection_errors import AuthenticationError
from wtwco_igloo.extensions.utils.errors.wtwco_igloo_errors import _log_and_get_exception


class _AuthenticationManagerWithRefresh(_AuthenticationManagerBase):
    def __init__(self, api_url: str, client_id: str, tenant_id: str):
        super().__init__(api_url, client_id, tenant_id)
        self._first_authentication: bool = True

    def _get_authenticated_client(self) -> AuthenticatedClient:
        if self._first_authentication:
            self._first_authentication = False
        else:
            self._refresh_token_if_needed()

        return super()._get_authenticated_client()

    def _refresh_token_if_needed(self) -> None:
        if isinstance(self._app, ConfidentialClientApplication):
            result = self._app.acquire_token_for_client(scopes=[self._scope])
        elif isinstance(self._app, PublicClientApplication):
            result = self._app.acquire_token_silent_with_error(
                scopes=[self._scope], account=self._app.get_accounts()[0]
            )

        if result.get("error_description") is not None or "access_token" not in result:
            raise _log_and_get_exception(
                AuthenticationError,
                "Failed to refresh the authentication token.",
                result.get("error"),
            )

        self._refresh_auth_client = (bool)(self._token != result["access_token"])
        self._token = result["access_token"]
