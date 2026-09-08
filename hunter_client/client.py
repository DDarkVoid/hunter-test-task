"""Modular Hunter API Client Facade."""
from hunter_client.http.base import HTTPTransport
from hunter_client.resources.domain import DomainResource
from hunter_client.resources.email import EmailResource

BASE_URL = 'https://api.hunter.io/v2'


class HunterClient(object):
    """Main client entry point."""

    def __init__(self, api_key: str, timeout: int = 10) -> None:
        """Initialize transport and resource modules."""
        self._transport = HTTPTransport(api_key, BASE_URL, timeout)
        self.email = EmailResource(self._transport)
        self.domain = DomainResource(self._transport)
