"""Service layer integrating HunterClient and DataStorage."""

from typing import Any, Dict

from hunter_client import HunterClient
from storage import DataStorage


class HunterService(object):
    """Service class for coordinating Hunter API operations and persistence."""

    def __init__(self, client: HunterClient, storage: DataStorage) -> None:
        """Initialize HunterService.

        Args:
            client: Hunter API client instance.
            storage: Data storage instance.
        """
        self._client = client
        self._storage = storage

    def verify_and_save_email(self, email: str) -> Dict[str, Any]:
        """Verify email using Hunter API and persist the result.

        Args:
            email: Email address to verify.

        Returns:
            Saved verification payload.
        """
        api_response = self._client.verify_email(email)
        record_id = 'email_verifier:{0}'.format(email)
        if self._storage.read(record_id) is not None:
            return self._storage.update(record_id, api_response)
        return self._storage.create(record_id, api_response)

    def search_and_save_domain(self, domain: str, limit: int = 10) -> Dict[str, Any]:
        """Search domain using Hunter API and persist the result.

        Args:
            domain: Domain name to search.
            limit: Maximum number of records to request.

        Returns:
            Saved domain search payload.
        """
        api_response = self._client.search_domain(domain, limit=limit)
        record_id = 'domain_search:{0}'.format(domain)
        if self._storage.read(record_id) is not None:
            return self._storage.update(record_id, api_response)
        return self._storage.create(record_id, api_response)
