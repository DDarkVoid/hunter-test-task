"""Domain search service."""
from hunter_client.client import HunterClient
from hunter_client.dto.domain import DomainSearchResultDTO
from repositories.domain_repository import DomainRepository


class DomainSearchService(object):
    """Orchestrates domain search."""

    def __init__(self, client: HunterClient, repository: DomainRepository) -> None:
        """Inject dependencies."""
        self._client = client
        self._repository = repository

    def execute(self, domain: str, limit: int = 10) -> DomainSearchResultDTO:
        """Search domain and persist result."""
        outcome = self._client.domain.search(domain, limit=limit)
        self._repository.save_search(domain, dict(outcome))
        return outcome
