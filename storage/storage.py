"""JSON File-backed CRUD Data Storage."""
import json
from pathlib import Path
from typing import Any, Dict, Optional


class StorageError(Exception):
    """Base exception for Storage errors."""


class DataStorage(object):
    """In-memory data storage synchronized with a JSON file."""

    def __init__(self, file_path: Path) -> None:
        """Initialize storage."""
        self._file_path = Path(file_path)
        self._storage_data: Dict[str, Dict[str, Any]] = {}
        self._load()

    def create(self, record_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a record."""
        if record_id in self._storage_data:
            raise StorageError(
                'Record with ID "{0}" already exists.'.format(record_id),
            )
        record_data = dict(payload)
        self._storage_data[record_id] = record_data
        self._save()
        return record_data

    def read(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Read a record."""
        record = self._storage_data.get(record_id)
        if record is None:
            return None
        return dict(record)

    def update(self, record_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record."""
        if record_id not in self._storage_data:
            raise StorageError(
                'Record with ID "{0}" not found.'.format(record_id),
            )
        record_data = dict(payload)
        self._storage_data[record_id] = record_data
        self._save()
        return record_data

    def delete(self, record_id: str) -> bool:
        """Delete a record."""
        removed = self._storage_data.pop(record_id, None)
        if removed is not None:
            self._save()
            return True
        return False

    def _load(self) -> None:
        """Load records from file."""
        if not self._file_path.exists():
            return
        try:
            with open(self._file_path, 'r', encoding='utf-8') as file_obj:
                raw_data = json.load(file_obj)
                if isinstance(raw_data, dict):
                    self._storage_data = raw_data
        except (json.JSONDecodeError, OSError) as exc:
            raise StorageError(
                'Failed to load storage file: {0}'.format(exc),
            ) from exc

    def _save(self) -> None:
        """Save records to file."""
        try:
            with open(self._file_path, 'w', encoding='utf-8') as file_obj:
                json.dump(self._storage_data, file_obj, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise StorageError(
                'Failed to write to storage file: {0}'.format(exc),
            ) from exc
