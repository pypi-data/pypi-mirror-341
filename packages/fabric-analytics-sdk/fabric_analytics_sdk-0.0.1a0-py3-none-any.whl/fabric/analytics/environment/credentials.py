import contextvars
from contextlib import contextmanager
from typing import Any

from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import ChainedTokenCredential, DefaultAzureCredential
from azure.identity._exceptions import CredentialUnavailableError
from fabric.analytics.environment.base.credentials import (
    IFabricAnalyticsTokenCredentialProviderPlugin,
)
from fabric.analytics.environment.plugin_provider import (
    BaseProvider,
    NoAvailableProvider,
)


class FabricAnalyticsTokenCredentials(ChainedTokenCredential):
    def __init__(self, fabric_analytics_credential=None, **kwargs: Any) -> None:
        fabric_analytics_credential = (
            fabric_analytics_credential
            if fabric_analytics_credential
            else FabricAnalyticsTokenCredentialProvider().provider_plugin
        )
        super().__init__(fabric_analytics_credential, DefaultAzureCredential(**kwargs))


context_credential = contextvars.ContextVar("context_credential", default=None)


@contextmanager
def SetFabricAnalyticsTokenCredentials(credential: TokenCredential):
    context_credential.set(credential)
    try:
        yield
    finally:
        context_credential.set(None)


class FabricAnalyticsTokenCredentialProvider(
    BaseProvider[IFabricAnalyticsTokenCredentialProviderPlugin]
):
    """
    Provide Fabric Context by selecting appropriate context provider plugins.
    Custom provider selection and initialization are both lazy.
    If you want initialization happen immediately, call load().

    We are not directly extending TokenCredential to avoid metaclass conflict,
    And TokenCredential is runtime checkable
    """

    plugin_entry_point_name = "fabric_analytics.token_credential_provider"

    def __init__(self):
        BaseProvider.__init__(self)
        self._register_entrypoints()

    @property
    def provider_plugin(self) -> IFabricAnalyticsTokenCredentialProviderPlugin:
        try:
            if context_credential.get() is not None:
                return context_credential.get()
            return super().provider_plugin
        except NoAvailableProvider as e:
            raise CredentialUnavailableError(str(e))
