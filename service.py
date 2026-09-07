"""Service layer integrating HunterClient and DataStorage."""

from typing import Any, Dict

from hunter_client import HunterClient
from storage import DataStorage


class HunterService(object):
    """Service class for coordinating Hunter API operations and persistence."""

    def __init__(self, client: HunterClient, storage: DataStorage) -> None:
        """Initialize HunterService."""
        self._client = client
        self._storage = storage

    def verify_and_save_email(self, email: str) -> Dict[str, Any]:
        """Verify email using Hunter API and persist the result."""
        api_response = self._client.email.verify(email)
        record_id = 'email_verifier:{0}'.format(email)
        if self._storage.read(record_id) is not None:
            return self._storage.update(record_id, api_response)
        return self._storage.create(record_id, api_response)

    def search_and_save_domain(self, domain: str, limit: int = 10) -> Dict[str, Any]:
        """Search domain using Hunter API and persist the result."""
        api_response = self._client.domain.search(domain, limit=limit)
        record_id = 'domain_search:{0}'.format(domain)
        if self._storage.read(record_id) is not None:
            return self._storage.update(record_id, api_response)
        return self._storage.create(record_id, api_response)
