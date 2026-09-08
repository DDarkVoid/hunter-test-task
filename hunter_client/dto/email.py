"""Email DTO definitions."""
from typing import TypedDict


class EmailVerificationDetailsDTO(TypedDict):
    """Payload nested in email verification response."""

    status: str
    score: int
    email: str


class EmailVerificationDTO(TypedDict):
    """Full response structure for email verification."""

    verification_payload: EmailVerificationDetailsDTO
