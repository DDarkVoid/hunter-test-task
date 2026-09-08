"""Email repository."""
from typing import Any, Dict, Optional

from storage.storage import DataStorage


class EmailRepository(object):
    """Repository for email records."""

    def __init__(self, storage: DataStorage) -> None:
        """Inject storage."""
        self._storage = storage

    def save_verification(self, email: str, payload: Dict[str, Any]) -> None:
        """Save verification payload."""
        record_id = 'email_verifier:{0}'.format(email)
        if self._storage.read(record_id) is not None:
            self._storage.update(record_id, payload)
        else:
            self._storage.create(record_id, payload)

    def get_verification(self, email: str) -> Optional[Dict[str, Any]]:
        """Get verification payload."""
        return self._storage.read('email_verifier:{0}'.format(email))
