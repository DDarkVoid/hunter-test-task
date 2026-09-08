"""Domain repository."""
from typing import Any, Dict, Optional

from storage.storage import DataStorage


class DomainRepository(object):
    """Repository for domain records."""

    def __init__(self, storage: DataStorage) -> None:
        """Inject storage."""
        self._storage = storage

    def save_search(self, domain: str, payload: Dict[str, Any]) -> None:
        """Save domain search payload."""
        record_id = 'domain_search:{0}'.format(domain)
        if self._storage.read(record_id) is not None:
            self._storage.update(record_id, payload)
        else:
            self._storage.create(record_id, payload)

    def get_search(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get domain search payload."""
        return self._storage.read('domain_search:{0}'.format(domain))
