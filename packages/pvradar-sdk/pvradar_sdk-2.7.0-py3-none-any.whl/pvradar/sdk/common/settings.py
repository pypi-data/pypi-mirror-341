import sys
from pathlib import Path
import tomllib
from typing import Optional
from platformdirs import user_config_path, user_data_path
from pydantic import BaseModel

from ..common.exceptions import PvradarSdkException

_sdk_toml_instance = None


def _get_settings_file_path() -> Path:
    return user_config_path('pvradar') / 'sdk.toml'


# the following class resembles the behavior of pydantic-settings
# but is more lightweight and does not require additional dependencies
class SdkSettings(BaseModel):
    outlet_base_url: str = 'https://api.pvradar.com/v2'
    outlet_token: str = ''
    platform_base_url: str = 'https://platform.pvradar.com/api'
    platform_username: str = ''
    platform_password: str = ''
    platform_token: str = ''
    caching_enabled: bool = True
    caching_kv_storage: str = 'lmdb'  # alternatives: 'memory', 'file', 'external'
    caching_lmdb_path: Optional[str] = None
    caching_lmdb_max_mbytes: Optional[int] = None
    caching_file_path: Optional[str] = None
    caching_max_age: int = 12 * 3600
    collect_api_metadata: bool = False
    default_flowchart_renderer: str = 'markdown'
    default_plot_renderer: str = 'plotly,matplotlib'

    @staticmethod
    def from_dict(d: dict) -> 'SdkSettings':
        d = d.copy()
        if 'token' in d:
            if 'outlet_token' not in d:
                d['outlet_token'] = d['token']
            if 'platform_token' not in d:
                d['platform_token'] = d['token']
            del d['token']

        # reduce potential side-effects of running tests
        if 'pytest' not in sys.modules:
            if 'caching_lmdb_path' not in d:
                d['caching_lmdb_path'] = str((user_data_path('pvradar') / 'lmdb_cache').absolute())
            if 'caching_file_path' not in d:
                d['caching_file_path'] = str((user_data_path('pvradar') / 'file_cache').absolute())

        if 'base_url' in d:
            raise ValueError('base_url is not a valid key, did you mean outlet_base_url instead?')

        result = SdkSettings(**d)

        for key in d:
            if not hasattr(result, key):
                raise ValueError(f'Unknown key: {key}')

        return result

    @staticmethod
    def from_config_path(path: str | Path) -> 'SdkSettings':
        try:
            with Path(path).open('rb') as conf_file:
                values = tomllib.load(conf_file)

                # always disable caching while running tests and reading global settings
                if 'pytest' in sys.modules:
                    values['caching_enabled'] = False

                return SdkSettings.from_dict(values)
        except OSError:
            raise PvradarSdkException(
                f'CRITICAL: No config found, expected file: {path} . '
                + 'Please contact PVRADAR tech. support if unsure what it is.'
            )
        except tomllib.TOMLDecodeError:
            raise PvradarSdkException(
                f'CRITICAL: Invalid config format found in file: {path} .' + 'Please contact PVRADAR tech. support.'
            )

    @staticmethod
    def instance() -> 'SdkSettings':
        global _sdk_toml_instance
        if _sdk_toml_instance is None:
            settings_path = _get_settings_file_path()
            _sdk_toml_instance = SdkSettings.from_config_path(settings_path)
        return _sdk_toml_instance
