"""Base HTTP transport."""
from typing import Any, Dict, Mapping

import requests

from hunter_client.http.exceptions import HunterHTTPError


class HTTPTransport(object):
    """Low-level HTTP transport with authentication."""

    def __init__(self, api_key: str, base_url: str, timeout: int = 10) -> None:
        """Initialize transport."""
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout
        self._session = requests.Session()

    def get(self, endpoint: str, query_params: Mapping[str, Any]) -> Dict[str, Any]:
        """Execute HTTP GET request."""
        url = '{0}/{1}'.format(self._base_url, endpoint)
        request_params = dict(query_params)
        request_params['api_key'] = self._api_key

        try:
            response = self._session.get(
                url,
                params=request_params,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            raise HunterHTTPError('HTTP request failed: {0}'.format(exc)) from exc

        response.raise_for_status()
        return response.json()
