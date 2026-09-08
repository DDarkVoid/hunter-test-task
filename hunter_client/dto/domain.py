"""Domain DTO definitions."""
from typing import List, TypedDict


class DomainEmailDTO(TypedDict):
    """Single email item in domain search."""

    email_address: str
    contact_type: str


class DomainPayloadDTO(TypedDict):
    """Payload nested in domain search response."""

    domain: str
    emails: List[DomainEmailDTO]


class DomainSearchResultDTO(TypedDict):
    """Full response structure for domain search."""

    domain_payload: DomainPayloadDTO
