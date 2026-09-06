"""Hunter.io API v2 Client implementation."""

from typing import Any, Dict, Optional

import requests

BASE_URL: str = 'https://api.hunter.io/v2'
DEFAULT_TIMEOUT: int = 10


class HunterClientError(Exception):
    """Base exception for HunterClient errors."""


class HunterClient(object):
    """HTTP Client for Hunter.io API v2."""

    def __init__(self, api_key: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize Hunter API client.

        Args:
            api_key: Hunter.io API key.
            timeout: HTTP request timeout in seconds.
        """
        self._api_key = api_key
        self._timeout = timeout
        self._session = requests.Session()

    def verify_email(self, email: str) -> Dict[str, Any]:
        """Verify an email address using Email Verifier endpoint.

        Args:
            email: Email address to verify.

        Returns:
            Dictionary with email verification data.
        """
        request_params = {'email': email}
        return self._get('email-verifier', request_params)

    def search_domain(self, domain: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Search email addresses belonging to a domain.

        Args:
            domain: Domain name to search.
            limit: Maximum number of results to return.

        Returns:
            Dictionary with domain search data.
        """
        request_params: Dict[str, Any] = {'domain': domain}
        if limit is not None:
            request_params['limit'] = limit
        return self._get('domain-search', request_params)

    def _get(self, endpoint: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a GET request to Hunter API endpoint.

        Args:
            endpoint: API endpoint relative path.
            request_params: Query parameters.

        Returns:
            Parsed JSON response as a dictionary.
        """
        url = '{0}/{1}'.format(BASE_URL, endpoint)
        query_params = dict(request_params)
        query_params['api_key'] = self._api_key
        return self._make_request(url, query_params)

    def _make_request(self, url: str, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute HTTP GET request and return JSON.

        Args:
            url: Full request URL.
            request_params: Query parameters.

        Returns:
            Response JSON as dict.

        Raises:
            HunterClientError: On request failure.
        """
        try:
            return self._process_response(self._session.get(
                url, params=request_params, timeout=self._timeout,
            ))
        except requests.RequestException as exc:
            raise HunterClientError(
                'Hunter API request failed: {0}'.format(exc),
            ) from exc

    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """Raise for status and return JSON.

        Args:
            response: HTTP response object.

        Returns:
            Parsed JSON dict.
        """
        response.raise_for_status()
        return response.json()
