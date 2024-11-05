import secrets
from typing import Annotated, Any, Literal, Optional

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',')]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='allow',
        env_ignore_empty=True,
    )
    api_name: str = 'globant'
    api_version: str = '0.0.1'
    api_host: str = 'localhost:8080'

    cors_allowed_origins: Annotated[
        list[AnyUrl] | list[str], BeforeValidator(parse_cors)
    ] = []

    secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 60 * 24 * 8
    log_level: str = 'INFO'

    environment: Literal['local', 'staging', 'production'] = 'local'
    is_local: bool = False
    postgres_database: str = 'globant'
    postgres_port: int = 5436
    postgres_user: str = 'globant'
    postgres_password: Optional[str] = None
    postgres_host: str = 'database'
    postgres_pool_size: int = 5
    verbose_db: bool = False

    max_batch_size: int = 2000

    @computed_field
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.environment == 'local':
            return f'http://{self.api_host}'
        return f'https://{self.api_host}'

    @computed_field
    @property
    def postgres_uri(self) -> PostgresDsn:
        host = 'localhost' if self.is_local else self.postgres_host
        return MultiHostUrl.build(
            scheme='postgresql+asyncpg',
            username=self.postgres_user,
            password=self.postgres_password,
            host=host,
            port=self.postgres_port,
            path=self.postgres_database,
        )


print(Settings())
