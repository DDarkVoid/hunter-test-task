"""Email verification service."""
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
