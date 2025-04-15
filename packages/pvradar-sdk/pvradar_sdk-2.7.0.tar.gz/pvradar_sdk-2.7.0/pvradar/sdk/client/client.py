import re
import tomllib
from typing import Any, Self, override
from pandas import DataFrame
from httpx import Response
from httpx._types import QueryParamTypes
import pandas as pd
import warnings

from ..common.exceptions import PvradarSdkException
from ..common.settings import SdkSettings, _get_settings_file_path
from ..common.pandas_utils import crop_by_interval
from .outlet.outlet_sync_client import ApiException, OutletSyncClient
from .platform.platform_sync_client import PlatformSyncClient

from .api_query import Query, ProviderType

_client_instance = None


class PvradarClient:
    def __init__(
        self,
        settings: SdkSettings,
    ):
        self.settings = settings
        self._outlet_client = None
        self._platform_client = None

    @override
    def __repr__(self) -> str:
        return f'<PvradarClient outlet={self.settings.outlet_base_url} platform={self.settings.platform_base_url}>'

    def _guess_provider(self, query: Query | str) -> ProviderType:
        path = query
        if isinstance(query, Query):
            if query.provider:
                return query.provider
            if query.project_id:
                return 'platform'
            path = query.path
        if 'assemblies' in path:
            return 'platform'
        return 'outlet'

    @classmethod
    def _make_outlet_client(cls, settings: SdkSettings) -> OutletSyncClient:
        return OutletSyncClient(
            token=settings.outlet_token,
            base_url=settings.outlet_base_url,
        )

    def _get_outlet_client(self) -> OutletSyncClient:
        if isinstance(self._outlet_client, OutletSyncClient):
            return self._outlet_client
        c = self._make_outlet_client(self.settings)
        self._outlet_client = c
        return c

    @classmethod
    def _make_platform_client(cls, settings: SdkSettings) -> PlatformSyncClient:
        return PlatformSyncClient(
            base_url=settings.platform_base_url,
            username=settings.platform_username,
            password=settings.platform_password,
            token=settings.platform_token,
        )

    def _get_platform_client(self) -> PlatformSyncClient:
        if isinstance(self._platform_client, PlatformSyncClient):
            return self._platform_client
        c = self._make_platform_client(self.settings)
        self._platform_client = c
        return c

    def _subclient(self, query: Query | str) -> OutletSyncClient | PlatformSyncClient:
        provider = self._guess_provider(query)
        if provider == 'outlet':
            return self._get_outlet_client()
        else:
            return self._get_platform_client()

    def get(self, query: str | Query, params: QueryParamTypes | None = None) -> Response:
        return self._subclient(query).get(query, params)

    def get_csv(self, query: str | Query, params: QueryParamTypes | None = None) -> str:
        return self._subclient(query).get_csv(query=query, params=params)

    def get_json(self, query: str | Query, params: QueryParamTypes | None = None) -> Any:
        return self._subclient(query).get_json(query=query, params=params)

    def get_df(
        self,
        query: str | Query,
        *,
        params: QueryParamTypes | None = None,
        crop_interval: pd.Interval | None = None,
    ) -> DataFrame:
        result = self._subclient(query).get_df(query=query, params=params)
        if crop_interval:
            result = crop_by_interval(result, crop_interval)
        return result

    @classmethod
    def from_config(cls, config_path_str='') -> Self:
        warnings.warn('from_config() is deprecated. Use instance() or PvradarClient(settings)', DeprecationWarning)
        return cls(SdkSettings.instance())

    @classmethod
    def instance(cls) -> Self:
        global _client_instance
        if not _client_instance:
            _client_instance = cls(SdkSettings.instance())
        return _client_instance

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        if not api_key:
            raise PvradarSdkException('API key cannot be empty.')
        current_contents = ''
        file_path = _get_settings_file_path()

        if file_path.exists():
            with file_path.open('r') as f:
                current_contents = f.read()

        if re.findall(r'^\s*(platform_|outlet_)token\s*=', current_contents, re.MULTILINE):
            raise PvradarSdkException(f'API key is already set for individual services. Please edit manually in "{file_path}"')

        if re.findall(r'^\s*token\s*=', current_contents, re.MULTILINE):
            current_contents = re.sub(r'^[ \t]*token\s*=.*$', f"token='{api_key}'", current_contents, flags=re.MULTILINE)
        else:
            current_contents += f"\ntoken='{api_key}'\n"

        print('validating... ', end='')

        values = tomllib.loads(current_contents)
        new_settings = SdkSettings.from_dict(values)
        outlet_client = cls._make_outlet_client(new_settings)
        try:
            summary = outlet_client.get_json('util/summary')
        except ApiException as e:
            print('failed')
            raise PvradarSdkException(str(e)) from e

        if not isinstance(summary, dict):
            raise PvradarSdkException('unexpected response')
        print('OK, server version: ' + summary.get('api_version', ''))

        with file_path.open('w') as f:
            f.write(current_contents)
