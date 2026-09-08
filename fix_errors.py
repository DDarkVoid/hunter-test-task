from pathlib import Path

files_fixes = {
    # 1. DTO (Исправление WPS110: замена запрещенных имен value, data, result)
    "hunter_client/dto/domain.py": '''"""Domain DTO definitions."""
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
''',

    "hunter_client/dto/email.py": '''"""Email DTO definitions."""
from typing import TypedDict


class EmailVerificationDetailsDTO(TypedDict):
    """Payload nested in email verification response."""

    status: str
    score: int
    email: str


class EmailVerificationDTO(TypedDict):
    """Full response structure for email verification."""

    verification_payload: EmailVerificationDetailsDTO
''',

    # 2. HTTP BASE (Исправление WPS110: params -> query_params, WPS229: try length)
    "hunter_client/http/base.py": '''"""Base HTTP transport."""
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
''',

    # 3. DOMAIN RESOURCE (Исправление mypy types & WPS110: params)
    "hunter_client/resources/domain.py": '''"""Domain resource endpoints."""
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
''',

    # 4. EMAIL RESOURCE (Синхронизация ключа DTO)
    "hunter_client/resources/email.py": '''"""Email resource endpoints."""
from hunter_client.dto.email import EmailVerificationDTO
from hunter_client.resources.base import BaseResource


class EmailResource(BaseResource):
    """Email-related API endpoints."""

    def verify(self, email: str) -> EmailVerificationDTO:
        """Verify an email address and return DTO."""
        response = self._transport.get('email-verifier', {'email': email})
        return EmailVerificationDTO(verification_payload=response['data'])
''',

    # 5. REPOSITORIES (Исправление WPS110: data -> payload)
    "repositories/domain_repository.py": '''"""Domain repository."""
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
''',

    "repositories/email_repository.py": '''"""Email repository."""
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
''',

    # 6. SERVICES (Исправление WPS110: result -> outcome)
    "service/domain_service.py": '''"""Domain search service."""
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
''',

    "service/email_service.py": '''"""Email verification service."""
from hunter_client.client import HunterClient
from hunter_client.dto.email import EmailVerificationDTO
from repositories.email_repository import EmailRepository


class EmailVerificationService(object):
    """Orchestrates email verification."""

    def __init__(self, client: HunterClient, repository: EmailRepository) -> None:
        """Inject dependencies."""
        self._client = client
        self._repository = repository

    def execute(self, email: str) -> EmailVerificationDTO:
        """Verify and persist result."""
        outcome = self._client.email.verify(email)
        self._repository.save_verification(email, dict(outcome))
        return outcome
''',

    # 7. MAIN.PY (Исправление WPS229 try body, WPS440 error overlap, WPS210 too many locals)
    "main.py": '''"""Application entry point."""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from hunter_client.client import HunterClient
from repositories.domain_repository import DomainRepository
from repositories.email_repository import EmailRepository
from service.domain_service import DomainSearchService
from service.email_service import EmailVerificationService
from storage.storage import DataStorage

logging.basicConfig(level=logging.INFO)


def _process_email(email_service: EmailVerificationService) -> None:
    """Process email verification flow."""
    logging.info('Verifying email...')
    try:
        email_res = email_service.execute('alexander.graham.bell@gmail.com')
    except Exception as email_err:
        logging.error('Email operation failed: {0}'.format(email_err))
    else:
        logging.info('Email Result: {0}'.format(email_res['verification_payload']))


def _process_domain(domain_service: DomainSearchService) -> None:
    """Process domain search flow."""
    logging.info('Searching domain...')
    try:
        domain_res = domain_service.execute('stripe.com', limit=5)
    except Exception as domain_err:
        logging.error('Domain operation failed: {0}'.format(domain_err))
    else:
        logging.info('Domain Result: {0}'.format(domain_res['domain_payload']))


def main() -> None:
    """Initialize dependencies and execution."""
    load_dotenv()
    api_key = os.getenv('HUNTER_API_KEY', 'demo_api_key')
    storage = DataStorage(Path('results.json'))
    client = HunterClient(api_key=api_key)

    email_service = EmailVerificationService(client, EmailRepository(storage))
    domain_service = DomainSearchService(client, DomainRepository(storage))

    _process_email(email_service)
    _process_domain(domain_service)


if __name__ == '__main__':
    main()
'''
}

for filepath, code in files_fixes.items():
    Path(filepath).write_text(code, encoding="utf-8")

print("Все патчи применены!")
