"""Application entry point."""
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
