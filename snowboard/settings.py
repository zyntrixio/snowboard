"""Snowboard Settings."""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

identity = DefaultAzureCredential()


class Settings(BaseSettings):
    """Snowboard Settings."""

    keyvault_url: AnyUrl = "https://uksouth-prod-qj46.vault.azure.net/"


settings = Settings()
keyvault_client = SecretClient(vault_url=str(settings.keyvault_url), credential=identity)
