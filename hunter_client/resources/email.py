"""Email resource endpoints."""
from hunter_client.dto.email import EmailVerificationDTO
from hunter_client.resources.base import BaseResource


class EmailResource(BaseResource):
    """Email-related API endpoints."""

    def verify(self, email: str) -> EmailVerificationDTO:
        """Verify an email address and return DTO."""
        response = self._transport.get('email-verifier', {'email': email})
        return EmailVerificationDTO(verification_payload=response['data'])
