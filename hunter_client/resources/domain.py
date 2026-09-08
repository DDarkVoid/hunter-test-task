"""Domain resource endpoints."""
from typing import Any, Dict, Optional

from hunter_client.dto.domain import DomainSearchResultDTO
from hunter_client.resources.base import BaseResource


class DomainResource(BaseResource):
    """Domain-related API endpoints."""

    def search(
        self,
        domain: str,
        limit: Optional[int] = None,
    ) -> DomainSearchResultDTO:
        """Search emails by domain."""
        query_params: Dict[str, Any] = {'domain': domain}
        if limit is not None:
            query_params['limit'] = limit
        response = self._transport.get('domain-search', query_params)
        return DomainSearchResultDTO(domain_payload=response['data'])
