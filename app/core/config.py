import tomllib
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_api_version() -> str:
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text())
    return f"/v{data['project']['version']}"


class Settings(BaseSettings):
    api_version: str = Field(
        default_factory=get_api_version, validation_alias='API_VERSION'
    )
    env: str = Field(default='development', validation_alias='ENV')
    postgres_user: str = Field(
        default='postgres', validation_alias='POSTGRES_USER'
    )
    postgres_password: str = Field(
        default='password', validation_alias='POSTGRES_PASSWORD'
    )
    postgres_host: str = Field(
        default='localhost', validation_alias='POSTGRES_HOST'
    )
    postgres_port: int = Field(default=5432, validation_alias='POSTGRES_PORT')
    postgres_db: str = Field(default='cnpj_api', validation_alias='POSTGRES_DB')
    
    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f'postgresql://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
