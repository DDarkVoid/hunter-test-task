"""Abstract base resource."""
from hunter_client.http.base import HTTPTransport


class BaseResource(object):
    """Base resource class for all API modules."""

    def __init__(self, transport: HTTPTransport) -> None:
        """Inject HTTP transport."""
        self._transport = transport
