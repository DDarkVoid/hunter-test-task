"""Hunter.io API v2 Client with scalable resource-based architecture."""

from typing import Any, Dict, Optional

import requests

BASE_URL: str = 'https://api.hunter.io/v2'
DEFAULT_TIMEOUT: int = 10


class HunterClientError(Exception):
    """Base exception for HunterClient errors."""


class _BaseEndpoint(object):
    """Base class for endpoint resource groups."""

    def __init__(self, client: 'HunterClient') -> None:
        """Initialize with parent client."""
        self._client = client


class EmailEndpoint(_BaseEndpoint):
    """Email-related endpoints."""

    def verify(self, email: str) -> Dict[str, Any]:
        """Verify an email address."""
        return self._client.get('email-verifier', {'email': email})


class DomainEndpoint(_BaseEndpoint):
    """Domain-related endpoints."""

    def search(self, domain: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Search emails by domain."""
        request_params: Dict[str, Any] = {'domain': domain}
        if limit is not None:
            request_params['limit'] = limit
        return self._client.get('domain-search', request_params)


class HunterClient(object):
    """Hunter.io API client with modular resource endpoints."""

    def __init__(self, api_key: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize client and resources."""
        self._api_key = api_key
        self._timeout = timeout
        self._session = requests.Session()

        # Resource endpoints
        self.email = EmailEndpoint(self)
        self.domain = DomainEndpoint(self)

    def get(self, endpoint: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GET request to Hunter API."""
        url = '{0}/{1}'.format(BASE_URL, endpoint)
        query_params = dict(request_params)
        query_params['api_key'] = self._api_key
        return self._make_request(url, query_params)

    def _make_request(self, url: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute HTTP GET and return JSON."""
        try:
            return self._send_request(url, request_params)
        except requests.RequestException as exc:
            raise HunterClientError(
                'Hunter API request failed: {0}'.format(exc),
            ) from exc

    def _send_request(self, url: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Send request and process response."""
        response = self._session.get(url, params=request_params, timeout=self._timeout)
        response.raise_for_status()
        return response.json()
