"""Application main entrypoint."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from hunter_client import HunterClient
from service import HunterService
from storage import DataStorage

logging.basicConfig(level=logging.INFO)


def _process_verification(service: HunterService, email: str) -> None:
    """Verify email and log result."""
    logging.info('Verifying email: {0}'.format(email))
    try:
        verification_result = service.verify_and_save_email(email)
    except Exception as error:
        logging.info('Operation failed: {0}'.format(error))
    else:
        logging.info('Email verification success!')
        logging.info('Result keys: {0}'.format(list(verification_result.keys())))


def _process_domain_search(service: HunterService, domain: str, limit: int) -> None:
    """Search domain and log result."""
    logging.info('Searching domain: {0}'.format(domain))
    try:
        domain_result = service.search_and_save_domain(domain, limit=limit)
    except Exception as error:
        logging.info('Operation failed: {0}'.format(error))
    else:
        logging.info('Domain search success!')
        logging.info('Result keys: {0}'.format(list(domain_result.keys())))


def run_example(service: HunterService) -> None:
    """Run verification and domain search examples."""
    _process_verification(service, 'alexander.graham.bell@gmail.com')
    _process_domain_search(service, 'stripe.com', 5)


def main() -> None:
    """Load configuration and run example."""
    load_dotenv()
    api_key = os.getenv('HUNTER_API_KEY', 'demo_api_key')
    storage_path = Path('results.json')
    storage = DataStorage(storage_path)
    client = HunterClient(api_key=api_key)
    service = HunterService(client=client, storage=storage)
    run_example(service)


if __name__ == '__main__':
    main()
