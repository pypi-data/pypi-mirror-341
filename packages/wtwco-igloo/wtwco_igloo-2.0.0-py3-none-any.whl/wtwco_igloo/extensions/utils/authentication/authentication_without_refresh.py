from wtwco_igloo.extensions.utils.authentication.authentication_base import _AuthenticationManagerBase


class _AuthenticationManagerWithoutRefresh(_AuthenticationManagerBase):
    def __init__(self, api_url: str, client_id: str, tenant_id: str):
        super().__init__(api_url, client_id, tenant_id)
